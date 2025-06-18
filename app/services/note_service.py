from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.note import CRUDNote
from app.schemas.note import NoteCreate
from app.models.note import Note


class NoteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_note(self, note_in: NoteCreate) -> Note:
        return await CRUDNote.create(self.db, note_in)

    async def get_note(self, note_id: int) -> Note | None:
        return await CRUDNote.get(self.db, note_id)

    async def list_notes(self) -> list[Note]:
        return await CRUDNote.get_all(self.db)