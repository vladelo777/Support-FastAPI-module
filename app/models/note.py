from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.models.attachment import Attachment


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    attachments = relationship("Attachment", back_populates="note", lazy="selectin")
    ticket = relationship("Ticket", back_populates="notes")
    author = relationship("User")
