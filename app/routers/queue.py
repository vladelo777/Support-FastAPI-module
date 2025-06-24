from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.queue import QueueCreate, QueueRead
from app.crud.queue import CRUDQueue

router = APIRouter(prefix="/queues", tags=["queues"])


@router.post("/", response_model=QueueRead)
async def create_queue(queue_in: QueueCreate, db: AsyncSession = Depends(get_db)):
    return await CRUDQueue.create(db, queue_in)


@router.get("/", response_model=List[QueueRead])
async def get_all_queues(db: AsyncSession = Depends(get_db)):
    return await CRUDQueue.get_all(db)


@router.get("/{queue_id}", response_model=QueueRead)
async def get_queue(queue_id: int, db: AsyncSession = Depends(get_db)):
    queue = await CRUDQueue.get(db, queue_id)
    if not queue:
        raise HTTPException(status_code=404, detail="Queue not found")
    return queue
