from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.note import CRUDNote
from app.schemas.note import NoteCreate
from app.models.note import Note


class NoteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_note(self, note_in: NoteCreate) -> Note:
        return await CRUDNote.create(self.db, note_in)

    async def get_notes_by_ticket(self, ticket_id: int) -> list[Note]:
        return await CRUDNote.get_by_ticket(self.db, ticket_id)