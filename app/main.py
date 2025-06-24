from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from app.routers import tickets, messages, note, ws_support, queue
from app.database import engine, Base
from app.email.email_task import periodic_email_check


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    email_task = asyncio.create_task(periodic_email_check())

    yield

    email_task.cancel()
    try:
        await email_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Support System", description="Made by Vladislav Lakhtionov", lifespan=lifespan)

app.include_router(tickets.router)
app.include_router(messages.router)
app.include_router(note.router)
app.include_router(ws_support.router)
app.include_router(queue.router)

# Для запуска – uvicorn app.main:app --reload
