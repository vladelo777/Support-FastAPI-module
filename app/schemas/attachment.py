from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AttachmentBase(BaseModel):
    filename: str
    content_type: Optional[str] = None

    message_id: Optional[int] = None
    note_id: Optional[int] = None


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentRead(AttachmentBase):
    id: int
    uploaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True
