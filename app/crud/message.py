from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.message import Message
from app.schemas.message import MessageCreate


class CRUDMessage:
    @staticmethod
    async def create(db: AsyncSession, message_in: MessageCreate) -> Message:
        message = Message(**message_in.dict())
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def get_by_ticket(db: AsyncSession, ticket_id: int) -> list[Message]:
        result = await db.execute(select(Message).where(Message.ticket_id == ticket_id))
        return result.scalars().all()
