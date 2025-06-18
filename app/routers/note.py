from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.note import NoteCreate, NoteRead
from app.services.note_service import NoteService
from app.database import get_db

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(note_in: NoteCreate, db: AsyncSession = Depends(get_db)):
    service = NoteService(db)
    note = await service.create_note(note_in)
    return note


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    service = NoteService(db)
    note = await service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteRead])
async def list_notes(db: AsyncSession = Depends(get_db)):
    service = NoteService(db)
    notes = await service.list_notes()
    return notes
