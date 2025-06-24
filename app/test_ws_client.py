import asyncio
import json
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws/support"

    async with websockets.connect(uri) as websocket:
        # Шаг 1: отправляем данные для создания тикета
        ticket_data = {
            "title": "Тестовый тикет через WS",
            "description": "Описание тикета",
            "priority": "Средний",
            "category": "Техподдержка",
            "client_id": 1,       # подставь существующий user_id
            "queue_id": 1         # подставь существующий queue_id
        }
        await websocket.send(json.dumps(ticket_data))
        print("Отправлен запрос на создание тикета")

        # Получаем ответ — id созданного тикета
        response = await websocket.recv()
        print(f"Получен ответ: {response}")
        response_data = json.loads(response)
        ticket_id = response_data.get("ticket_id")

        if not ticket_id:
            print("Не удалось получить ticket_id, завершаем.")
            return

        print(f"Тикет создан с id={ticket_id}")

        # Теперь можно отправлять сообщения в чат с этим ticket_id
        # Пример: отправим одно сообщение
        message_data = {
            "ticket_id": ticket_id,
            "author_id": 1,  # подставь id автора (client или agent)
            "content": "Привет, это первое сообщение в чате!",
            "is_from_agent": False
        }
        await websocket.send(json.dumps(message_data))
        print("Отправлено сообщение в чат")

        # Получаем рассылку (то же сообщение)
        msg_response = await websocket.recv()
        print(f"Получено сообщение: {msg_response}")

asyncio.run(test_ws())