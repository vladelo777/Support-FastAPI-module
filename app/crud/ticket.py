from sqlalchemy.orm import Session
from sqlalchemy.future import select
from datetime import datetime

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket:
    @staticmethod
    async def create(
            db: Session,
            ticket_in: TicketCreate,
            frt_deadline: datetime,
            ttr_deadline: datetime,
    ) -> Ticket:
        ticket = Ticket(
            **ticket_in.model_dump(),
            frt_deadline=frt_deadline,
            ttr_deadline=ttr_deadline,
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    async def get(db: Session, ticket_id: int) -> Ticket | None:
        result = db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: Session) -> list[Ticket]:
        result = db.execute(select(Ticket))
        return result.scalars().all()

    @staticmethod
    async def update(db: Session, ticket: Ticket, ticket_in: TicketUpdate) -> Ticket:
        for field, value in ticket_in.dict(exclude_unset=True).items():
            setattr(ticket, field, value)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    async def delete(db: Session, ticket: Ticket) -> None:
        db.delete(ticket)
        db.commit()
