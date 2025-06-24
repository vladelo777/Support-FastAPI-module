import imaplib
import email
import asyncio
from email.header import decode_header
from email.utils import parseaddr
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.ticket import TicketCreate
from app.services.ticket_service import TicketService
from app.database import async_session
from app.config import IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD, QUEUE_ID, DEFAULT_CLIENT_ID


def decode_mime_words(s):
    decoded_fragments = decode_header(s)
    return ''.join([
        fragment.decode(encoding or 'utf-8') if isinstance(fragment, bytes) else fragment
        for fragment, encoding in decoded_fragments
    ])


def get_email_body(message):
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and part.get_payload(decode=True):
                return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
    else:
        return message.get_payload(decode=True).decode(message.get_content_charset() or 'utf-8')
    return ""


async def process_email(msg, db: AsyncSession):
    subject = decode_mime_words(msg["Subject"] or "Без темы")
    from_email = parseaddr(msg.get("From"))[1]
    body = get_email_body(msg)

    ticket_data = TicketCreate(
        title=subject,
        description=body,
        client_id=DEFAULT_CLIENT_ID,
        category='Вопрос с почты',
        queue_id=QUEUE_ID
    )
    service = TicketService(db)
    await service.create_ticket(ticket_data)
    print(f"Создан тикет от {from_email}: {subject}")


async def check_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')  # Только непрочитанные
    if status != "OK":
        print("Не удалось получить письма.")
        return

    email_ids = messages[0].split()
    if not email_ids:
        print("Новых писем нет.")
        return

    async with async_session() as db:
        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    await process_email(msg, db)

    mail.logout()


if __name__ == "__main__":
    asyncio.run(check_email())

# Для запуска – python -m app.email.email_processor
