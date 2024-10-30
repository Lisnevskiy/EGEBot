import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
