from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.attachment import AttachmentRead


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    ticket_id: int
    author_id: int


class NoteRead(NoteBase):
    id: int
    ticket_id: int
    author_id: int
    created_at: datetime
    attachments: Optional[List[AttachmentRead]] = []

    class Config:
        from_attributes = True
