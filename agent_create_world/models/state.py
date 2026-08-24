from typing import List, Optional

from pydantic import BaseModel

class AgentState(BaseModel):
    '''agent 运行状态'''
    user_query: str
    messages: List[dict] = []
    current_step: int = 0
    is_complete: bool = False
    final_answer: Optional[str] = None

