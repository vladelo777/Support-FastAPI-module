from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database import Base


class UserRole(PyEnum):
    CLIENT = "client"
    AGENT = "agent"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)

    tickets_created = relationship("Ticket", foreign_keys="Ticket.client_id", back_populates="client")
    tickets_assigned = relationship("Ticket", foreign_keys="Ticket.agent_id", back_populates="agent")