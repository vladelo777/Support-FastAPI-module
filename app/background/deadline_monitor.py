import asyncio
import logging
from sqlalchemy import select
from datetime import datetime, timedelta

from app.database import async_session
from app.models.ticket import TicketStatus, Ticket

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def format_time_delta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    minutes = total_seconds // 60
    if minutes < 60:
        return f"{minutes} мин"
    else:
        hours = minutes // 60
        return f"{hours} ч {minutes % 60} мин"


async def monitor_deadlines():
    while True:
        try:
            async with async_session() as session:
                now = datetime.now()

                result = await session.execute(
                    select(Ticket).where(Ticket.status != TicketStatus.CLOSED)
                )
                tickets = result.scalars().all()

                found_violations = False

                for ticket in tickets:
                    messages = []

                    if ticket.frt_deadline:
                        if now > ticket.frt_deadline:
                            messages.append("⛔ FRT просрочен")
                        elif now + timedelta(hours=1) > ticket.frt_deadline:
                            remaining = format_time_delta(ticket.frt_deadline - now)
                            messages.append(f"🚨 FRT скоро истечёт (осталось {remaining})")

                    if ticket.ttr_deadline:
                        if now > ticket.ttr_deadline:
                            messages.append("⛔ TTR просрочен")
                        elif now + timedelta(hours=1) > ticket.ttr_deadline:
                            remaining = format_time_delta(ticket.ttr_deadline - now)
                            messages.append(f"🚨 TTR скоро истечёт (осталось {remaining})")

                    if messages:
                        found_violations = True
                        logger.warning(
                            f"[🧾 Ticket #{ticket.id} | {ticket.title}] " + " | ".join(messages)
                        )

                if not found_violations:
                    logger.info("✅ Все дедлайны соблюдены для всех тикетов")

        except Exception:
            logger.exception("❌ Ошибка при проверке дедлайнов")

        await asyncio.sleep(60)
