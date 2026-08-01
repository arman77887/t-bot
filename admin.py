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
    async def handle_admin_callbacks(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        query = update.callback_query

        if not self.is_admin(query.from_user.id):

            await query.answer("Access Denied", show_alert=True)
            return

        await query.answer()

        data = query.data

        if data == "admin_users":

            total = self.db.get_total_users()

            await query.edit_message_text(
                f"👥 Total Users: {total}",
                reply_markup=Keyboards.admin_menu()
            )

        elif data == "admin_premium":

            premium = self.db.get_total_premium()

            await query.edit_message_text(
                f"⭐ Premium Users: {premium}",
                reply_markup=Keyboards.admin_menu()
            )

        elif data == "admin_stats":

            users = self.db.get_total_users()
            premium = self.db.get_total_premium()
            balance = self.db.get_total_balance()

            text = f"""
📊 Bot Statistics

👥 Users: {users}

⭐ Premium: {premium}

💰 Total Balance:
${balance}
"""

            await query.edit_message_text(
                text,
                reply_markup=Keyboards.admin_menu()
            )

        elif data == "admin_ban":

            await query.edit_message_text(
                "Send:\n\n/ban USER_ID\n\nor\n\n/unban USER_ID"
            )

        else:

            await query.edit_message_text(
                "Unknown Admin Action"
            )


    async def ban_user(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        if not self.is_admin(update.effective_user.id):
            return

        if len(context.args) != 1:

            await update.message.reply_text(
                "Usage:\n/ban USER_ID"
            )

            return

        user_id = int(context.args[0])

        self.db.ban_user(user_id)

        await update.message.reply_text(
            "✅ User Banned"
        )


    async def unban_user(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        if not self.is_admin(update.effective_user.id):
            return

        if len(context.args) != 1:

            await update.message.reply_text(
                "Usage:\n/unban USER_ID"
            )

            return

        user_id = int(context.args[0])

        self.db.unban_user(user_id)

        await update.message.reply_text(
            "✅ User Unbanned"
        )


    async def give_premium(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        if not self.is_admin(update.effective_user.id):
            return

        if len(context.args) != 1:

            await update.message.reply_text(
                "Usage:\n/premium USER_ID"
            )

            return

        user_id = int(context.args[0])

        self.db.set_premium(user_id, True)

        await update.message.reply_text(
            "⭐ Premium Activated"
        )
