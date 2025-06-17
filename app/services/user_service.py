from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import CRUDUser
from app.schemas.user import UserCreate
from app.models.user import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_in: UserCreate) -> User:
        return await CRUDUser.create(self.db, user_in)

    async def get_user_by_email(self, email: str) -> User | None:
        return await CRUDUser.get_by_email(self.db, email)

    async def get_user(self, user_id: int) -> User | None:
        return await CRUDUser.get(self.db, user_id)
