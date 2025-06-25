from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from app.database import Base


class TicketStatus(PyEnum):
    OPEN = "Открыт"
    IN_PROGRESS = "В работе"
    WAITING = "Ожидает клиента"
    CLOSED = "Закрыт"


class TicketPriority(PyEnum):
    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"
    URGENT = "Срочный"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    category = Column(String, nullable=True)

    queue_id = Column(Integer, ForeignKey("queues.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    frt_deadline = Column(DateTime, nullable=True)
    ttr_deadline = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    queue = relationship("Queue", back_populates="tickets")
    client = relationship("User", foreign_keys=[client_id])
    agent = relationship("User", foreign_keys=[agent_id])
    messages = relationship("Message", back_populates="ticket", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="ticket", cascade="all, delete-orphan")
