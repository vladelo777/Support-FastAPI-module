from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.message import MessageCreate, MessageRead
from app.services.message_service import MessageService
from app.database import get_db

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(message_in: MessageCreate, db: AsyncSession = Depends(get_db)):
    service = MessageService(db)
    message = await service.create_message(message_in)
    return message


@router.get("/ticket/{ticket_id}", response_model=List[MessageRead])
async def get_messages_by_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    service = MessageService(db)
    messages = await service.get_messages_by_ticket(ticket_id)
    if messages is None:
        raise HTTPException(status_code=404, detail="Messages not found")
    return messages
