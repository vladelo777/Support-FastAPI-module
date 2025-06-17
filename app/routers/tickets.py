from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services.ticket_service import TicketService
from app.database import get_db

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_in: TicketCreate, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    ticket = await service.create_ticket(ticket_in)
    return ticket


@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    ticket = await service.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketRead)
async def update_ticket(ticket_id: int, ticket_in: TicketUpdate, db: AsyncSession = Depends(get_db)):
    service = TicketService(db)
    ticket = await service.update_ticket(ticket_id, ticket_in)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket