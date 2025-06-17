from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.ticket import CRUDTicket
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.models.ticket import Ticket


class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_ticket(self, ticket_in: TicketCreate) -> Ticket:
        return await CRUDTicket.create(self.db, ticket_in)

    async def get_ticket(self, ticket_id: int) -> Ticket | None:
        return await CRUDTicket.get(self.db, ticket_id)

    async def update_ticket(self, ticket_id: int, ticket_in: TicketUpdate) -> Ticket | None:
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            return None
        return await CRUDTicket.update(self.db, ticket, ticket_in)
