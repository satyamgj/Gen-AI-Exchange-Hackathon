from pydantic import BaseModel


class chatResponse(BaseModel):
    question: str
    response: str