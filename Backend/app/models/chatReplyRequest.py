from pydantic import BaseModel
from typing import List


class chatReplyRequest(BaseModel):
    query: str
    past_replies:List[str]  # Correct way to type a list of strings
