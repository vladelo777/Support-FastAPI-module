from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.queue import Queue
from app.schemas.queue import QueueCreate


class CRUDQueue:
    @staticmethod
    async def create(db: AsyncSession, queue_in: QueueCreate) -> Queue:
        queue = Queue(**queue_in.dict())
        db.add(queue)
        await db.commit()
        await db.refresh(queue)
        return queue

    @staticmethod
    async def get(db: AsyncSession, queue_id: int) -> Queue | None:
        result = await db.execute(select(Queue).where(Queue.id == queue_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Queue]:
        result = await db.execute(select(Queue))
        return result.scalars().all()
