from pydantic import BaseModel


class QueueBase(BaseModel):
    name: str
    description: str | None = None


class QueueCreate(QueueBase):
    pass


class QueueRead(QueueBase):
    id: int

    class Config:
        orm_mode = True
