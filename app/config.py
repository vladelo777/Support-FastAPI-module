from dotenv import load_dotenv
import os

load_dotenv()

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
QUEUE_ID = int(os.getenv("QUEUE_ID", 5))
DEFAULT_CLIENT_ID = int(os.getenv("DEFAULT_CLIENT_ID", 1))
