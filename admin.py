from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import Config
from database import Database
from keyboards import Keyboards


class AdminHandler:

    def __init__(self):
        self.db = Database()

    def is_admin(self, user_id: int):
        return user_id in Config.ADMIN_IDS

    async def admin_menu(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        if not self.is_admin(update.effective_user.id):

            await update.message.reply_text(
                "❌ Access Denied."
            )

            return

        total_users = self.db.get_total_users()
        premium = self.db.get_total_premium()
        balance = self.db.get_total_balance()

        text = f"""
🛠 Admin Panel

👥 Users : {total_users}

⭐ Premium : {premium}

💰 Balance : ${balance}
"""

        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=Keyboards.admin_menu()
        )
