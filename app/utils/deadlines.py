from datetime import datetime, timedelta

from app.models.ticket import TicketPriority


def get_deadlines_by_priority(priority: TicketPriority, created_at: datetime) -> tuple[datetime, datetime]:
    if priority == TicketPriority.LOW:
        frt = created_at + timedelta(hours=8)
        ttr = created_at + timedelta(days=3)
    elif priority == TicketPriority.MEDIUM:
        frt = created_at + timedelta(hours=4)
        ttr = created_at + timedelta(days=2)
    elif priority == TicketPriority.HIGH:
        frt = created_at + timedelta(hours=1)
        ttr = created_at + timedelta(days=1)
    elif priority == TicketPriority.URGENT:
        frt = created_at + timedelta(minutes=30)
        ttr = created_at + timedelta(hours=12)
    else:
        # fallback
        frt = created_at + timedelta(hours=4)
        ttr = created_at + timedelta(days=2)

    return frt, ttr
