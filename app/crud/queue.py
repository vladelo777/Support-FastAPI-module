from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.queue import Queue
from app.schemas.queue import QueueCreate


class CRUDQueue:
    @staticmethod
    async def create(db: Session, queue_in: QueueCreate) -> Queue:
        queue = Queue(**queue_in.dict())
        db.add(queue)
        db.commit()
        db.refresh(queue)
        return queue

    @staticmethod
    async def get(db: Session, queue_id: int) -> Queue | None:
        result = db.execute(select(Queue).where(Queue.id == queue_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: Session) -> list[Queue]:
        result = db.execute(select(Queue))
        return result.scalars().all()
