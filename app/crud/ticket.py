from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket:
    @staticmethod
    async def create(db: AsyncSession, ticket_in: TicketCreate) -> Ticket:
        ticket = Ticket(**ticket_in.dict())
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def get(db: AsyncSession, ticket_id: int) -> Ticket | None:
        result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Ticket]:
        result = await db.execute(select(Ticket))
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, ticket: Ticket, ticket_in: TicketUpdate) -> Ticket:
        for field, value in ticket_in.dict(exclude_unset=True).items():
            setattr(ticket, field, value)
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def delete(db: AsyncSession, ticket: Ticket) -> None:
        await db.delete(ticket)
        await db.commit()
