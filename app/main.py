from fastapi import FastAPI

from app.routers import tickets, messages, note
from app.database import engine, Base
from app import models

app = FastAPI(title="Support System", description="Made by Vladislav Lakhtionov")


@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(tickets.router)
app.include_router(messages.router)
app.include_router(note.router)
