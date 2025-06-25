from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser:
    @staticmethod
    async def create(db: Session, user_in: UserCreate) -> User:
        user = User(**user_in.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    async def get_by_email(db: Session, email: str) -> User | None:
        result = db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    @staticmethod
    async def get(db: Session, user_id: int) -> User | None:
        result = db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
