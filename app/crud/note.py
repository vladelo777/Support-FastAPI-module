from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.note import Note
from app.schemas.note import NoteCreate


class CRUDNote:
    @staticmethod
    async def create(db: Session, note_in: NoteCreate) -> Note:
        note = Note(**note_in.dict())
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    async def get(db: Session, note_id: int) -> Note | None:
        result = db.execute(select(Note).where(Note.id == note_id))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: Session) -> list[Note]:
        result = db.execute(select(Note))
        return result.scalars().all()

    @staticmethod
    async def get_by_ticket(db: Session, ticket_id: int) -> list[Note]:
        result = db.execute(select(Note).where(Note.ticket_id == ticket_id).order_by(Note.created_at))
        return result.scalars().all()

    @staticmethod
    async def delete(db: Session, note: Note) -> None:
        db.delete(note)
        db.commit()
