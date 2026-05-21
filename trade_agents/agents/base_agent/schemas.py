from pydantic import BaseModel, Field
from typing import List, Optional

class RandomNumberGenerator(BaseModel):
    num: int

class TestSchema(BaseModel):
    test: str = "schema"

class ThoughtStep(BaseModel):
    reasoning: str = Field(description="智能体当前步骤的中文推理理由")

class ChainOfThoughtSchema(BaseModel):
    thoughts: List[ThoughtStep] = Field(description="智能体逐步中文推理过程")
    final_answer: str = Field(description="推理后的中文最终回答")

class Action(BaseModel):
    name: str = Field(description="要执行的动作名称")
    input: Optional[str] = Field(description="指定动作所需的输入（如有）")

class ReActSchema(BaseModel):
    thought: str = Field(description="智能体对当前状态和下一步行动的中文推理")
    action: Optional[Action] = Field(description="要执行的动作（如有）")
    observation: Optional[str] = Field(description="动作执行后的观察结果")
    final_answer: Optional[str] = Field(description="任务完成时的中文最终回答")
