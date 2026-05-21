from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict, Any

class PerceptionSchema(BaseModel):
    monologue: str = Field(..., description="智能体对当前市场/环境状态的中文内心独白")
    strategy: List[str] = Field(..., description="智能体基于当前市场/环境状态制定的中文策略列表")
    confidence: float = Field(..., ge=0.0, le=1.0, description="0.0 到 1.0 之间的信心分数")

class ReflectionSchema(BaseModel):
    reflection: str = Field(..., description="对观察结果和行动表现的中文反思")
    strategy_update: List[str] = Field(..., description="基于反思和上一轮策略更新后的中文策略列表")
    self_reward: float = Field(..., description="0.0 到 1.0 之间的自评分数")
