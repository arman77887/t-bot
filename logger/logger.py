import logging
import os
from logging.handlers import RotatingFileHandler
from config import Config

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/bot.log"

logger = logging.getLogger("ai_bot")
logger.setLevel(getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO))

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
