from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.attachment import AttachmentRead


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
    attachments: Optional[List[AttachmentRead]] = []

    class Config:
        from_attributes = True
