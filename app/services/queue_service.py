from sqlalchemy.orm import Session
from app.crud.queue import CRUDQueue
from app.schemas.queue import QueueCreate
from app.models.queue import Queue


class QueueService:
    def __init__(self, db: Session):
        self.db = db

    async def create_queue(self, queue_in: QueueCreate) -> Queue:
        return await CRUDQueue.create(self.db, queue_in)

    async def get_queue(self, queue_id: int) -> Queue | None:
        return await CRUDQueue.get(self.db, queue_id)

    async def get_all_queues(self) -> list[Queue]:
        return await CRUDQueue.get_all(self.db)