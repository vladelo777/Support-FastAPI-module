from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
# from app.database import async_session
# from app.database import get_db
from app.schemas.message import MessageCreate
from app.crud.message import CRUDMessage
from app.models.user import User
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, ticket_id: int, websocket: WebSocket):
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = []
        self.active_connections[ticket_id].append(websocket)

    def disconnect(self, ticket_id: int, websocket: WebSocket):
        self.active_connections[ticket_id].remove(websocket)
        if not self.active_connections[ticket_id]:
            del self.active_connections[ticket_id]

    async def broadcast(self, ticket_id: int, message: dict):
        for connection in self.active_connections.get(ticket_id, []):
            await connection.send_json(message)


manager = ConnectionManager()
