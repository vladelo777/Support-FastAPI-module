from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.note import Note
from app.schemas.note import NoteCreate


class CRUDNote:
    @staticmethod
    async def create(db: AsyncSession, note_in: NoteCreate) -> Note:
        note = Note(**note_in.dict())
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    @staticmethod
    async def get_by_ticket(db: AsyncSession, ticket_id: int) -> list[Note]:
        result = await db.execute(select(Note).where(Note.ticket_id == ticket_id))
        return result.scalars().all()
