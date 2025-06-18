from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    content: str
    is_from_agent: bool = False


class MessageCreate(MessageBase):
    ticket_id: int
    author_id: int


class MessageRead(MessageBase):
    id: int
    ticket_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
