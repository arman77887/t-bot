import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ==========================
    # Telegram
    # ==========================
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = [
        int(x)
        for x in os.getenv("ADMIN_IDS", "").split(",")
        if x.strip()
    ]

    # ==========================
    # Database
    # ==========================
    DATABASE_NAME = "database/bot.db"

    # ==========================
    # AI Keys
    # ==========================
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    GROK_API_KEY = os.getenv("GROK_API_KEY")

    # ==========================
    # Default AI
    # ==========================
    DEFAULT_MODEL = "gemini"

    # ==========================
    # Limits
    # ==========================
    DAILY_FREE_LIMIT = 20

    PREMIUM_DAILY_LIMIT = 999999

    # ==========================
    # Premium
    # ==========================
    PREMIUM_PRICE = 10

    PREMIUM_CURRENCY = "USD"

    # ==========================
    # Available Models
    # ==========================
    AVAILABLE_MODELS = {

        "gemini": {
            "name": "Google Gemini",
            "enabled": bool(GEMINI_API_KEY)
        },

        "chatgpt": {
            "name": "OpenAI ChatGPT",
            "enabled": bool(OPENAI_API_KEY)
        },

        "claude": {
            "name": "Claude",
            "enabled": bool(CLAUDE_API_KEY)
        },

        "deepseek": {
            "name": "DeepSeek",
            "enabled": bool(DEEPSEEK_API_KEY)
        },

        "grok": {
            "name": "Grok",
            "enabled": bool(GROK_API_KEY)
        }

    }
