from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.attachment import AttachmentRead
from app.services.attachment_service import AttachmentService
from typing import List

router = APIRouter(prefix="/attachments", tags=["attachments"])


@router.post("/upload/message/{message_id}", response_model=AttachmentRead)
async def upload_to_message(message_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    service = AttachmentService(db)
    return await service.save_file(file, message_id=message_id)


@router.post("/upload/note/{note_id}", response_model=AttachmentRead)
async def upload_to_note(note_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    service = AttachmentService(db)
    return await service.save_file(file, note_id=note_id)


@router.get("/message/{message_id}", response_model=List[AttachmentRead])
async def list_by_message(message_id: int, db: AsyncSession = Depends(get_db)):
    service = AttachmentService(db)
    return await service.get_by_message(message_id)


@router.get("/note/{note_id}", response_model=List[AttachmentRead])
async def list_by_note(note_id: int, db: AsyncSession = Depends(get_db)):
    service = AttachmentService(db)
    return await service.get_by_note(note_id)
