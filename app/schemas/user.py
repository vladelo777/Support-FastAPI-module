from pydantic import BaseModel, EmailStr
from typing import Literal


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: Literal["client", "agent"] = "client"


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
