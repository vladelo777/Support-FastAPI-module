from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime

from app.crud.ticket import CRUDTicket
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticket import Ticket, TicketPriority
from app.crud.queue import CRUDQueue
from app.utils.deadlines import get_deadlines_by_priority
from app.crud.user import CRUDUser
from app.models.user import UserRole

FRT_TTR_DEADLINES = {
    TicketPriority.LOW: (timedelta(hours=12), timedelta(days=3)),
    TicketPriority.MEDIUM: (timedelta(hours=4), timedelta(days=2)),
    TicketPriority.HIGH: (timedelta(hours=2), timedelta(days=1)),
    TicketPriority.URGENT: (timedelta(minutes=30), timedelta(hours=8)),
}


class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_ticket(self, ticket_in: TicketCreate) -> Ticket:
        # Проверка на очередь
        queue = await CRUDQueue.get(self.db, ticket_in.queue_id)
        if not queue:
            raise HTTPException(status_code=400, detail="Очередь с таким ID не существует")

        # Проверка клиента
        client = await CRUDUser.get(self.db, ticket_in.client_id)
        if not client:
            raise HTTPException(status_code=400, detail="Данный client_id не существует!")
        if client.role != UserRole.client:
            raise HTTPException(status_code=400, detail="Данный user не является клиентом!")

        # 🎯 Вычисляем дедлайны
        now = datetime.now()
        frt_deadline, ttr_deadline = get_deadlines_by_priority(ticket_in.priority, now)

        return await CRUDTicket.create(self.db, ticket_in, frt_deadline=frt_deadline, ttr_deadline=ttr_deadline)

    async def get_all_tickets(self) -> list[Ticket]:
        return await CRUDTicket.get_all(self.db)

    async def get_ticket(self, ticket_id: int) -> Ticket | None:
        return await CRUDTicket.get(self.db, ticket_id)

    async def update_ticket(self, ticket_id: int, ticket_in: TicketUpdate) -> Ticket | None:
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            return None

        ## Проверка агента
        if ticket_in.agent_id is not None:
            agent = await CRUDUser.get(self.db, ticket_in.agent_id)
            if not agent:
                raise HTTPException(status_code=400, detail="Данный agent_id не существует!")
            if agent.role != UserRole.agent:
                raise HTTPException(status_code=400, detail="Данный user не является агентом!")

        return await CRUDTicket.update(self.db, ticket, ticket_in)
