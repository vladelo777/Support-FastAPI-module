# app/models/attachment.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, nullable=False)
    content_type = Column(String, nullable=False)

    message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=True)

    message = relationship("Message", back_populates="attachments")
    note = relationship("Note", back_populates="attachments")
