import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.routers import tickets, messages, note, ws_support, queue, attachments
from app.database import engine, Base
from app.email.email_task import periodic_email_check
from app.background.deadline_monitor import monitor_deadlines


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создание папки для вложений, если нет
    os.makedirs("uploads", exist_ok=True)

    # 🔁 Запуск фоновых задач
    email_task = asyncio.create_task(periodic_email_check())
    monitor_task = asyncio.create_task(monitor_deadlines())

    yield

    # ⛔️ Остановка фоновых задач
    for task in (email_task, monitor_task):
        task.cancel()
        try:
            await task
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

# Для запуска – uvicorn app.main:app --reload
