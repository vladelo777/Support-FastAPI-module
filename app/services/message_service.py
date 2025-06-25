from sqlalchemy.orm import Session
from app.crud.message import CRUDMessage
from app.schemas.message import MessageCreate
from app.models.message import Message


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    async def create_message(self, message_in: MessageCreate) -> Message:
        return await CRUDMessage.create(self.db, message_in)

    async def get_messages_by_ticket(self, ticket_id: int) -> list[Message]:
        return await CRUDMessage.get_by_ticket(self.db, ticket_id)