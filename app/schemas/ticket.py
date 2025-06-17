from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Literal["Низкий", "Средний", "Высокий", "Срочный"] = "Средний"
    category: Optional[str] = None
    queue_id: Optional[int] = None


class TicketCreate(TicketBase):
    client_id: int


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["Открыт", "В работе", "Ожидает клиента", "Закрыт"]] = None
    priority: Optional[Literal["Низкий", "Средний", "Высокий", "Срочный"]] = None
    category: Optional[str] = None
    agent_id: Optional[int] = None
    queue_id: Optional[int] = None


class TicketRead(TicketBase):
    id: int
    status: Literal["Открыт", "В работе", "Ожидает клиента", "Закрыт"]
    client_id: int
    agent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
