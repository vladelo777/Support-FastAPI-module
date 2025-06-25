from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.attachment import Attachment
from app.schemas.attachment import AttachmentCreate


class CRUDAttachment:
    @staticmethod
    async def create(db: Session, attachment_in: AttachmentCreate) -> Attachment:
        attachment = Attachment(**attachment_in.model_dump())
        db.add(attachment)
        db.commit()
        db.refresh(attachment)
        return attachment

    @staticmethod
    async def get_by_message(db: Session, message_id: int) -> list[Attachment]:
        result = db.execute(
            select(Attachment).where(Attachment.message_id == message_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_note(db: Session, note_id: int) -> list[Attachment]:
        result = db.execute(
            select(Attachment).where(Attachment.note_id == note_id)
        )
        return result.scalars().all()
