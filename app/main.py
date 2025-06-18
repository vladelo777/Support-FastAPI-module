from fastapi import FastAPI
from app.routers import tickets, messages
from app.database import engine, Base

from app import models

app = FastAPI(title="Support System")


# Создаем таблицы при старте приложения
@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Подключаем роутеры
app.include_router(tickets.router)
app.include_router(messages.router)
