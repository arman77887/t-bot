import logging
import os
from config import Config

# logs ফোল্ডার না থাকলে তৈরি করবে
os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/bot.log"

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AI-Telegram-Bot")
