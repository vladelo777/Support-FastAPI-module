from pydantic import BaseModel
from datetime import datetime


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

    class Config:
        from_attributes = True