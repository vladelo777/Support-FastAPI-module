import asyncio
from app.email.email_processor import check_email


async def periodic_email_check():
    while True:
        print("🔄 Checking email...")
        try:
            await check_email()
        except Exception as e:
            print(f"❌ Ошибка при проверке email: {e}")
        await asyncio.sleep(30)  # интервал между проверками в секундах
