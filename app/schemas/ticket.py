from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.ticket import TicketPriority, TicketStatus


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.LOW
    category: Optional[str] = None
    queue_id: int


class TicketCreate(TicketBase):
    client_id: int


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    category: Optional[str] = None
    agent_id: int


class TicketRead(TicketBase):
    id: int
    status: TicketStatus
    client_id: int
    agent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True
