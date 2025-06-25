from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_NAME = os.getenv("DATABASE_NAME")

IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
QUEUE_ID = int(os.getenv("QUEUE_ID", 5))
DEFAULT_CLIENT_ID = int(os.getenv("DEFAULT_CLIENT_ID", 1))
