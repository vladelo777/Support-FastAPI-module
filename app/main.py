from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
import os

from app.routers import tickets, messages, note, ws_support, queue, attachments
from app.database import engine, Base
from app.email.email_task import periodic_email_check


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создание папки для вложений, если нет
    os.makedirs("uploads", exist_ok=True)

    # Запуск фоновой задачи (email polling)
    email_task = asyncio.create_task(periodic_email_check())

    yield

    # Остановка фоновой задачи
    email_task.cancel()
    try:
        await email_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Support System",
    description="Made by Vladislav Lakhtionov",
    lifespan=lifespan
)

# 📁 Static-файлы: отдаём загруженные вложения
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(tickets.router)
app.include_router(messages.router)
app.include_router(note.router)
app.include_router(ws_support.router)
app.include_router(queue.router)
app.include_router(attachments.router)

# Для запуска: uvicorn app.main:app --reload
