from typing import Optional
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attachment import Attachment
from app.schemas.attachment import AttachmentCreate
from app.crud.attachment import CRUDAttachment
import shutil
import uuid
import os


class AttachmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_file(
            self,
            file: UploadFile,
            message_id: Optional[int] = None,
            note_id: Optional[int] = None
    ) -> Attachment:
        # Получаем расширение файла
        file_extension = os.path.splitext(file.filename)[1]
        # Генерируем уникальное имя файла
        unique_name = f"{uuid.uuid4()}{file_extension}"
        # Путь сохранения
        file_path = os.path.join("uploads", unique_name)

        # Сохраняем файл на диск
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Создаём DTO для создания Attachment
        attachment_in = AttachmentCreate(
            filename=unique_name,
            message_id=message_id,
            note_id=note_id,
            content_type=file.content_type
        )

        return await CRUDAttachment.create(self.db, attachment_in)

    async def get_by_message(self, message_id: int):
        return await CRUDAttachment.get_by_message(self.db, message_id)

    async def get_by_note(self, note_id: int):
        return await CRUDAttachment.get_by_note(self.db, note_id)
