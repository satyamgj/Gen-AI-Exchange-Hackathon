from pydantic import BaseModel


class chatRequest(BaseModel):
    query: str
