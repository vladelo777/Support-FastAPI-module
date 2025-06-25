from app.database import SessionLocal
from app.models.queue import Queue
from sqlalchemy import select


def seed_queues():
    with SessionLocal() as session:
        result = session.execute(select(Queue))
        existing = result.scalars().all()

        if existing:
            print("Очереди уже существуют")
            return

        queues = [
            Queue(name="Техническая поддержка", description='Очередь для вопросов по оказанию технической поддержки'),
            Queue(name="Биллинг", description='Очередь для вопросов по оплате'),
            Queue(name="Логистика", description='Очередь для вопросов по доставке'),
            Queue(name="Общие вопросы", description='Очередь для общих вопросов'),
            Queue(name="Вопросы с почты", description='Очередь для вопросов, падающих с почты'),
        ]
        session.add_all(queues)
        session.commit()
        print("Очереди успешно добавлены")


if __name__ == "__main__":
    seed_queues()

# Для запуска – python -m app.seed_queues