import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # Admin
    ADMIN_IDS = [
        int(x) for x in os.getenv("ADMIN_IDS", "").split(",")
        if x.strip().isdigit()
    ]

    # AI Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    GROK_API_KEY = os.getenv("GROK_API_KEY", "")

    # Stripe
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

    # Database
    DATABASE_NAME = os.getenv("DATABASE_NAME", "database/bot.db")

    # Limits
    DAILY_FREE_LIMIT = int(os.getenv("DAILY_FREE_LIMIT", "20"))
    PREMIUM_DAILY_LIMIT = int(os.getenv("PREMIUM_DAILY_LIMIT", "1000"))

    # Default AI
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini").lower()

    # Premium
    PREMIUM_PRICE = float(os.getenv("PREMIUM_PRICE", "15"))
    PREMIUM_CURRENCY = os.getenv("PREMIUM_CURRENCY", "USD")

    # Referral
    REFERRAL_BONUS = float(os.getenv("REFERRAL_BONUS", "1"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    AVAILABLE_MODELS = {
        "gemini": bool(GEMINI_API_KEY),
        "chatgpt": bool(OPENAI_API_KEY),
        "claude": bool(CLAUDE_API_KEY),
        "deepseek": bool(DEEPSEEK_API_KEY),
        "grok": bool(GROK_API_KEY),
    }
