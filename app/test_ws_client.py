import asyncio
import json
import websockets


async def test_ws(ticket_id: int, user_id: int, message: str):
    uri = f"ws://localhost:8000/ws/support/{ticket_id}?user_id={user_id}"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")

        # Отправляем JSON-сообщение
        await websocket.send(json.dumps({
            "ticket_id": ticket_id,
            "author_id": user_id,
            "is_from_agent": False,
            "content": message
        }))
        print(f">>> Sent JSON: {message}")

        # Получаем ответ от сервера
        response = await websocket.recv()
        print(f"<<< Received: {response}")


if __name__ == "__main__":
    asyncio.run(test_ws(ticket_id=1, user_id=2, message="Привет, это тестовое сообщение!"))
