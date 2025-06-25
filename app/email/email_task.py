import asyncio
import logging
from app.email.email_processor import check_email

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)


async def periodic_email_check():
    while True:
        logger.info("🔄 Проверка новых писем...")
        try:
            check_email()
        except Exception:
            logger.exception("❌ Ошибка при проверке email")
        await asyncio.sleep(60)  # Интервал между проверками в секундах
