# TradeAgents 中文版

TradeAgents 是一个用于构建智能体市场仿真的框架。它把经济学机制、智能体认知流程、大语言模型推理、短期/长期记忆和可选知识库结合在一起，用来模拟交易、拍卖、群聊讨论等多智能体场景。

<p align="center">
  <img src="assets/tradeagents.jpg" alt="TradeAgents" width="80%" height="80%">
</p>

## 主要特性

- **市场仿真**：支持拍卖、群聊等多智能体环境，用于观察买方/卖方策略与市场动态。
- **大模型智能体**：通过 LLM 进行感知、行动和反思，提示词已改为简体中文。
- **记忆系统**：每个智能体会使用短期认知记忆和长期情景记忆，依赖 PostgreSQL/pgvector 存储。
- **可选知识库**：项目包含向量知识库模块，但默认配置未启用；配置 `agent_config.knowledge_base` 后才会检索知识库文档。
- **中文输出**：智能体提示词、人格、schema 描述、默认商品、群聊话题和主要运行日志已中文化。

## 知识库说明

当前默认配置文件 `trade_agents/orchestrators/orchestrator_config.yaml` 中：

```yaml
agent_config:
  knowledge_base: ""
```

这表示默认运行时**不会使用外部知识库**。但项目已经内置知识库能力：

- `trade_agents/memory/knowledge_base.py`：负责知识入库、切分、向量化和存储。
- `trade_agents/memory/vector_search.py`：负责向量检索。
- `trade_agents/memory/knowledge_base_agent.py`：把知识库检索能力接入智能体。
- `trade_agents/agents/market_agent.py`：如果智能体带有 `knowledge_agent`，感知阶段会把检索到的文档放入提示词。

如果要启用知识库，需要先准备对应前缀的数据表并写入知识，然后把配置改成对应前缀，例如：

```yaml
agent_config:
  knowledge_base: "market_kb"
```

这样系统会尝试读取 `market_kb_knowledge_objects` 和 `market_kb_knowledge_chunks` 等表。

## 安装

### 环境要求

- Python 3.8+
- PostgreSQL（如果启用数据库记忆/知识库）
- 依赖包见 `requirements.txt`
- 大模型 API Key（例如 OpenAI、Anthropic 或 LiteLLM 兼容服务）

### 安装步骤

```sh
cd /Users/tongmeixuan/Desktop/tradeagents-main
pip install -r requirements.txt
pip install -e .
cp .env.example .env
```

然后根据本机环境修改 `.env` 中的 API Key 和数据库配置。

## 运行仿真

推荐从项目根目录运行：

```sh
cd /Users/tongmeixuan/Desktop/tradeagents-main
bash run_simulation.sh
```

脚本会自动检查并启动群聊 API、仪表盘，然后运行主编排器。

## 常用配置

主配置文件：

```sh
trade_agents/orchestrators/orchestrator_config.yaml
```

常见字段：

- `num_agents`：智能体数量。
- `max_rounds`：仿真总轮数。
- `environment_order`：运行环境顺序，例如 `group_chat`、`auction`。
- `agent_config.good_name`：交易商品名称，当前默认是 `草莓`。
- `agent_config.knowledge_base`：知识库表前缀，空字符串表示不启用知识库。
- `llm_configs`：大模型配置。

## 中文化范围

已中文化的核心部分包括：

- 智能体默认系统提示词：`trade_agents/agents/configs/prompts/default_prompt.yaml`
- 市场智能体感知/行动/反思提示词：`trade_agents/agents/configs/prompts/market_agent_prompt.yaml`
- 人格模板和已有生成角色：`trade_agents/agents/personas/`
- 群聊、聊天、拍卖相关 schema 描述
- 默认商品和群聊初始话题
- 主要终端日志、运行脚本和总结输出

## 故障排查

### 数据库连接失败

检查 `.env` 和 `trade_agents/memory/memory_config.yaml` 中的数据库地址、端口、用户名和密码是否正确。

### 知识库没有生效

确认：

1. `agent_config.knowledge_base` 不是空字符串。
2. 对应知识库表已经创建并有数据。
3. embedding 服务配置可用，或允许使用 mock embedding。

### 智能体仍输出英文

确认你运行的是当前项目目录，并且没有加载旧的缓存/旧日志。中文控制主要来自提示词和 schema 描述，字段名仍会保持英文以兼容 JSON 结构。

## 许可证

本项目遵循原项目许可证，详见 `LICENSE`。
