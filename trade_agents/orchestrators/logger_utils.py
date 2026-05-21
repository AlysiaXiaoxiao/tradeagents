import logging
from typing import List
import json
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.logging import RichHandler
from rich.align import Align
from rich.box import HEAVY

console = Console(force_terminal=True, color_system="auto")

def print_ascii_art():
    ascii_art = pyfiglet.figlet_format("tradeagents", font="slant")
    console.print(f"[cyan]{ascii_art}[/cyan]")

def setup_logger(name: str = "MarketSimulation", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Add RichHandler to log to console with rich formatting and enable markup
    handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True  # Enable markup interpretation
    )
    logger.addHandler(handler)
    
    # Prevent propagation to avoid double logging
    logger.propagate = False
    
    return logger

# Create a single, centralized logger instance
orchestration_logger = setup_logger()

def json_to_markdown(data: dict) -> str:
    """Convert a JSON object to markdown format"""
    key_map = {
        "monologue": "内心独白",
        "strategy": "策略",
        "confidence": "信心分数",
        "reflection": "反思",
        "strategy_update": "策略更新",
        "self_reward": "自评奖励",
        "action": "行动",
        "content": "内容",
        "thoughts": "思考过程",
        "final_answer": "最终回答",
        "reasoning": "推理",
    }
    markdown = ""
    for key, value in data.items():
        title = key_map.get(key, key)
        markdown += f"### {title}\n"
        if isinstance(value, list):
            for item in value:
                markdown += f"- {item}\n"
        else:
            markdown += f"{value}\n"
        markdown += "\n"
    return markdown

def log_persona(logger: logging.Logger, agent_index: int, persona: str):
    header = f"[bold yellow]🎭 智能体 {agent_index:02d} 人格:[/bold yellow]\n"
    text = Text.from_markup(header)
    text.append(persona)
    panel = Panel(
        Align.left(text),
        border_style="yellow",
        box=HEAVY,
        width=80
    )
    console.print(panel)

def log_perception(logger: logging.Logger, agent_id: int, perception: str):
    try:
        perception_dict = json.loads(perception) if isinstance(perception, str) else perception
        markdown = json_to_markdown(perception_dict)
        header = f"[bold cyan]👁️  智能体 {agent_id:02d} 感知:[/bold cyan]\n"
        text = Text.from_markup(header)
        text.append(markdown)
        panel = Panel(
            Align.left(text),
            border_style="cyan",
            box=HEAVY,
            width=80
        )
        console.print(panel)
    except Exception as e:
        console.print(f"[bold blue]👁️ 智能体 {agent_id} 感知:[/bold blue]\n[cyan]{perception}[/cyan]")

def log_reflection(logger: logging.Logger, agent_id: int, reflection: str):
    try:
        reflection_dict = json.loads(reflection) if isinstance(reflection, str) else reflection
        markdown = json_to_markdown(reflection_dict)
        header = f"[bold magenta]💭 智能体 {agent_id:02d} 反思:[/bold magenta]\n"
        text = Text.from_markup(header)
        text.append(markdown)
        panel = Panel(
            Align.left(text),
            border_style="magenta",
            box=HEAVY,
            width=80
        )
        console.print(panel)
    except Exception as e:
        console.print(f"[bold magenta]💭 智能体 {agent_id} 反思:[/bold magenta]\n[magenta]{reflection}[/magenta]")

def log_section(logger: logging.Logger, message: str):
    border = "=" * 70
    logger.info(f"[magenta]{border}[/magenta]")
    logger.info(f"[yellow]🔥 {message.upper()} 🔥[/yellow]")
    logger.info(f"[magenta]{border}[/magenta]")

def log_round(logger: logging.Logger, round_num: int):
    logger.info(f"[green]🔔 第 {round_num:02d} 轮开始 🔔[/green]")
    logger.info(f"[cyan]🎲 市场动态开始演化！ 🎲[/cyan]")

def log_agent_init(logger: logging.Logger, agent_id: int, is_buyer: bool, persona):
    agent_type = "🛒 买方" if is_buyer else "💼 卖方"
    trader_type = " | ".join(persona.trader_type)
    logger.info(f"[blue]🤖 智能体 {agent_id:02d} | {agent_type} | {trader_type} | 已初始化[/blue]")

def log_environment_setup(logger: logging.Logger, env_name: str):
    logger.info(f"[green]🏛️ 进入 {env_name.upper()} 环境 🏛️[/green]")
    logger.info(f"[yellow]📈 市场力量正在塑造决策 📉[/yellow]")

def log_completion(logger: logging.Logger, message: str):
    logger.info(f"[green]🎉 {message} 🚀[/green]")

def log_skipped(logger: logging.Logger, message: str):
    logger.info(f"[red]⏭️ {message}（出现意外市场变化）[/red]")

def log_running(logger: logging.Logger, env_name: str):
    logger.info(f"[green]🏁 {env_name} 市场已启动 🏁[/green]")
    logger.info(f"[yellow]💥 准备观察经济互动！ 💥[/yellow]")

def log_raw_action(logger: logging.Logger, agent_id: int, action: dict):
    logger.info(f"[black on yellow]🔧 智能体 {agent_id} 执行: [/black on yellow]")
    logger.info(f"[yellow]{action}[/yellow]")

def log_action(logger: logging.Logger, agent_id: int, action: str):
    if "Bid" in action:
        emoji = "💰"
        color = "green"
    elif "Ask" in action:
        emoji = "💵"
        color = "yellow"
    elif "reflects" in action.lower() or "反思" in action:
        emoji = "💭"
        color = "magenta"
    elif "perceives" in action.lower() or "感知" in action:
        emoji = "👁️"
        color = "cyan"
    else:
        emoji = "🔧"
        color = "white"
    logger.info(f"[{color}]{emoji} 智能体 {agent_id:02d} 执行: {action}[/{color}]")

def log_market_update(logger: logging.Logger, update: str):
    logger.info(f"[black on cyan]📢 市场洞察:[/black on cyan]")
    logger.info(f"[cyan]{update}[/cyan]")

def log_trade(logger: logging.Logger, buyer_id: int, seller_id: int, item: str, price: float):
    logger.info(f"[black on green]💰 交易提醒 💰[/black on green]")
    logger.info(f"[green]🤝 智能体 {buyer_id:02d} 以 ${price:.2f} 从智能体 {seller_id:02d} 处买入 {item}[/green]")

def log_leaderboard(logger: logging.Logger, rankings: list):
    header = f"[bold black on yellow]🏆 表现排名 🏆[/bold black on yellow]"
    content = ""
    for rank, (agent_id, score) in enumerate(rankings, 1):
        indicator = ["🥇", "🥈", "🥉"][rank-1] if rank <= 3 else "  "
        color = ["yellow", "white", "red"][rank-1] if rank <= 3 else "blue"
        content += f"[{color}]{indicator} 第 {rank} 名：智能体 {agent_id:02d} - ${score:.2f}[/{color}]\n"
    text = Text.from_markup(content)
    panel = Panel(
        Align.left(text),
        title=header,
        title_align="left",
        border_style="yellow",
        box=HEAVY,
        width=80
    )
    console.print(panel)

def log_topic_proposal(logger: logging.Logger, cohort_id: str, proposer_id: int, topic: str):
    header = f"[bold white on blue]📢 话题提议 - {cohort_id.upper()} 📢[/bold white on blue]"
    proposer_info = f"[bold]🎯 提议者：智能体 {proposer_id:02d}[/bold]"
    topic_info = f"[cyan]💬 话题：{topic}[/cyan]"
    text = Text.from_markup(f"{proposer_info}\n\n{topic_info}")
    panel = Panel(
        Align.left(text),
        border_style="blue",
        box=HEAVY,
        width=80,
        title=header,
        title_align="left"
    )
    console.print(panel)

def log_group_message(logger: logging.Logger, cohort_id: str, agent_id: int, message: str, sub_round: int):
    agent_colors = [
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "red",
        "white"
    ]
    color = agent_colors[agent_id % len(agent_colors)]
    header = f"[bold black on white]💬 {cohort_id.upper()} - 第 {sub_round} 小轮[/bold black on white]"
    agent_info = f"[bold {color}]🤖 智能体 {agent_id:02d} 发言:[/bold {color}]"
    text = Text.from_markup(f"{agent_info}\n\n{message}")
    panel = Panel(
        Align.left(text),
        border_style=color,
        box=HEAVY,
        width=80,
        title=header,
        title_align="left"
    )
    console.print(panel)

def log_cohort_formation(logger: logging.Logger, cohort_id: str, agent_indices: List[int]):
    logger.info(f"[black on green]🎯 群组形成 🎯[/black on green]")
    logger.info(f"[green]📋 {cohort_id.upper()}：智能体 {agent_indices}[/green]")
    logger.info(f"[green]{'─' * 50}[/green]")

def log_sub_round_start(logger: logging.Logger, cohort_id: str, sub_round: int):
    logger.info(f"[black on yellow]🔄 第 {sub_round} 小轮 - {cohort_id.upper()} 🔄[/black on yellow]")
    logger.info(f"[yellow]{'─' * 50}[/yellow]")

def log_group_chat_summary(logger: logging.Logger, cohort_id: str, messages_count: int, topic: str):
    header = f"[bold white on magenta]📊 群聊总结 - {cohort_id.upper()} 📊[/bold white on magenta]"
    content = f"[magenta]📝 消息总数：{messages_count}\n\n💭 讨论话题：{topic}[/magenta]"
    text = Text.from_markup(content)
    panel = Panel(
        Align.left(text),
        border_style="magenta",
        box=HEAVY,
        width=80,
        title=header,
        title_align="left"
    )
    console.print(panel)

# Example usage:

if __name__ == "__main__":
    print_ascii_art()
