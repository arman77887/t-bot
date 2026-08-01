import hashlib
import random
import string
from datetime import datetime
from functools import wraps

from config import Config


class Utils:

    @staticmethod
    def generate_session_id(user_id: int) -> str:
        raw = f"{user_id}{datetime.now().timestamp()}{random.random()}"
        return hashlib.md5(raw.encode()).hexdigest()

    @staticmethod
    def truncate_text(text: str, max_length: int = 4000):
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def split_message(text: str, size: int = 4000):
        return [
            text[i:i + size]
            for i in range(0, len(text), size)
        ]

    @staticmethod
    def escape_markdown(text: str):
        chars = r"_*[]()~`>#+-=|{}.!"
        for c in chars:
            text = text.replace(c, "\\" + c)
        return text

    @staticmethod
    def random_string(length=8):
        return "".join(
            random.choice(
                string.ascii_letters + string.digits
            )
            for _ in range(length)
        )

    @staticmethod
    def format_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def admin_required(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):

        user_id = update.effective_user.id

        if user_id not in Config.ADMIN_IDS:
            if update.message:
                await update.message.reply_text(
                    "❌ You are not an admin."
                )
            elif update.callback_query:
                await update.callback_query.answer(
                    "Not allowed!",
                    show_alert=True
                )
            return

        return await func(update, context, *args, **kwargs)

    return wrapper
