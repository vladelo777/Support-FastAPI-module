import asyncio
from app.database import async_session
from app.models.queue import Queue
from sqlalchemy import select


async def seed_queues():
    async with async_session() as session:
        result = await session.execute(select(Queue))
        existing = result.scalars().all()

        if existing:
            print("Очереди уже существуют")
            return

        queues = [
            Queue(name="Техническая поддержка", description='Очередь для вопросов по оказанию технической поддержки'),
            Queue(name="Биллинг", description='Очередь для вопросов по оплате'),
            Queue(name="Логистика", description='Очередь для вопросов по доставке'),
            Queue(name="Общие вопросы", description='Очередь для общих вопросов'),
        ]
        session.add_all(queues)
        await session.commit()
        print("Очереди успешно добавлены")


if __name__ == "__main__":
    asyncio.run(seed_queues())
