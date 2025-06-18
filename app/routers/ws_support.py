from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# from app.database import async_session
from app.database import get_db
from app.websockets.ws_support import manager
from app.schemas.message import MessageCreate
from app.crud.message import CRUDMessage

router = APIRouter()


@router.websocket("/ws/support/{ticket_id}")
async def websocket_endpoint(websocket: WebSocket, ticket_id: int, db: AsyncSession = Depends(get_db)):
    await manager.connect(ticket_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message_in = MessageCreate(**data)
            message = await CRUDMessage.create(db, message_in)

            # Подготовим сообщение для отправки всем участникам тикета
            payload = {
                "id": message.id,
                "ticket_id": message.ticket_id,
                "author_id": message.author_id,
                "is_from_agent": message.is_from_agent,
                "content": message.content,
                "created_at": str(message.created_at)
            }

            await manager.broadcast(ticket_id, payload)
    except WebSocketDisconnect:
        manager.disconnect(ticket_id, websocket)
