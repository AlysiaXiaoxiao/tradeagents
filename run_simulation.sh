#!/bin/bash

# 运行市场仿真的脚本：并行编排、仪表盘与耗时统计

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# File names for the Python scripts
ORCHESTRATOR_SCRIPT="trade_agents/orchestrators/meta_orchestrator.py"
DASHBOARD_SCRIPT="trade_agents/agents/db/dashboard/dashboard.py"
GROUPCHAT_API_SCRIPT="trade_agents/orchestrators/group_chat/groupchat_api.py"
DASHBOARD_PORT=8000
GROUPCHAT_API_PORT=8001

# Check if the Python scripts exist
for script in "$ORCHESTRATOR_SCRIPT" "$DASHBOARD_SCRIPT" "$GROUPCHAT_API_SCRIPT"; do
    if [ ! -f "$script" ]; then
        echo "错误：未找到 $script！"
        exit 1
    fi
done

check_api_health() {
    local port=$1
    local retries=3
    local wait_time=2
    
    for i in $(seq 1 $retries); do
        if curl -s "http://localhost:$port/health" > /dev/null; then
            return 0  # API is healthy
        fi
        echo "第 $i 次尝试：等待 API 健康检查通过……"
        sleep $wait_time
    done
    return 1  # API failed health check
}

# Check and start GroupChat API if needed
if check_port $GROUPCHAT_API_PORT; then
    echo "群聊 API 已在 http://localhost:$GROUPCHAT_API_PORT 运行"
    GROUPCHAT_STARTED=false
else
    echo "正在启动群聊 API……"
    python3 "$GROUPCHAT_API_SCRIPT" &
    GROUPCHAT_PID=$!
    GROUPCHAT_STARTED=true

    # Check if API becomes healthy
    if ! check_api_health $GROUPCHAT_API_PORT; then
        echo "群聊 API 启动失败，正在结束进程……"
        kill $GROUPCHAT_PID
        exit 1
    fi
    echo "群聊 API 已运行：http://localhost:$GROUPCHAT_API_PORT"
fi

# Check and start dashboard if needed
if check_port $DASHBOARD_PORT; then
    echo "仪表盘已在 http://localhost:$DASHBOARD_PORT 运行"
    DASHBOARD_STARTED=false
else
    echo "正在启动仪表盘……"
    python3 "$DASHBOARD_SCRIPT" &
    DASHBOARD_PID=$!
    DASHBOARD_STARTED=true

    sleep 2
    echo "仪表盘已运行：http://localhost:$DASHBOARD_PORT"
fi

# Get the start time
start_time=$(date +%s)

# Run the orchestrator script
echo "正在启动并行编排市场仿真……"
python3 "$ORCHESTRATOR_SCRIPT" 2>&1 | tee simulation_output.log

orchestrator_exit_code=${PIPESTATUS[0]}

# Get the end time and calculate duration
end_time=$(date +%s)
duration=$((end_time - start_time))

# Print results
echo "----------------------------------------"
echo "仿真结束，退出码：$orchestrator_exit_code"
echo "总执行时间：$duration 秒"
echo "----------------------------------------"
echo "完整输出已保存到 simulation_output.log"
echo "----------------------------------------"

if [ $orchestrator_exit_code -ne 0 ]; then
    echo "错误：编排器脚本失败，退出码 $orchestrator_exit_code"
else
    echo "仿真成功完成。"
fi

# Cleanup services that we started
if [ "$DASHBOARD_STARTED" = true ] || [ "$GROUPCHAT_STARTED" = true ]; then
    echo "按 Enter 停止本脚本启动的服务并退出。"
    read

    if [ "$DASHBOARD_STARTED" = true ]; then
        kill $DASHBOARD_PID
        echo "仪表盘已停止。"
    fi

    if [ "$GROUPCHAT_STARTED" = true ]; then
        kill $GROUPCHAT_PID
        echo "群聊 API 已停止。"
    fi
else
    echo "相关服务原本已在运行，将继续保持运行。"
fi

exit $orchestrator_exit_code
