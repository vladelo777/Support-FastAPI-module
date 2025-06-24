from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.ticket_service import TicketService
from app.websockets.ws_support import manager
from app.schemas.ticket import TicketCreate
from app.schemas.message import MessageCreate
from app.crud.message import CRUDMessage

router = APIRouter()


@router.websocket("/ws/support")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    """
    WebSocket endpoint для поддержки клиентов.

    Протокол взаимодействия:
    1. Клиент устанавливает соединение.
    2. Клиент отправляет JSON с данными для создания тикета, например:
       {
         "title": "Проблема с оплатой",
         "description": "Не получается оплатить заказ",
         "status": "OPEN",
         "priority": "MEDIUM",
         "category": "Техподдержка",
         "queue_id": 1,
         "client_id": 123
       }
    3. Сервер создает тикет и отправляет обратно JSON с ID тикета:
       {"ticket_id": 42}
    4. Клиент может отправлять сообщения, сервер рассылает их всем подключенным к тикету.

    Закрытие соединения:
    - При отключении WebSocket соединения оно удаляется из активных.

    Ошибки:
    - При некорректных данных сервер может закрыть соединение с ошибкой.
    """
    await websocket.accept()

    # Ожидаем первое сообщение — это должны быть данные для создания тикета
    data = await websocket.receive_json()

    # Создаем тикет на основе полученных данных
    ticket_create_data = TicketCreate(**data)

    service = TicketService(db)
    ticket = await service.create_ticket(ticket_create_data)

    # Отправляем клиенту id созданного тикета
    await websocket.send_json({"ticket_id": ticket.id})

    # Регистрируем соединение по ticket.id
    await manager.connect(ticket.id, websocket)

    try:
        while True:
            message_data = await websocket.receive_json()
            message_in = MessageCreate(**message_data)
            message = await CRUDMessage.create(db, message_in)

            payload = {
                "id": message.id,
                "ticket_id": message.ticket_id,
                "author_id": message.author_id,
                "is_from_agent": message.is_from_agent,
                "content": message.content,
                "created_at": str(message.created_at)
            }

            await manager.broadcast(ticket.id, payload)

    except WebSocketDisconnect:
        manager.disconnect(ticket.id, websocket)
