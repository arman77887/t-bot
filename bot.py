import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import Config
from database import Database
from handlers import AIHandler
from admin import AdminHandler
from keyboards import Keyboards
from logger.logger import logger
from errors.error_handler import ErrorHandler


db = Database()
ai = AIHandler()
admin = AdminHandler()
error_handler = ErrorHandler()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    db.register_user(
        user.id,
        user.username,
        user.first_name,
        user.last_name
    )

    text = (
        f"👋 Welcome {user.first_name}\n\n"
        "🤖 Multi AI Telegram Bot\n\n"
        "Supported Models:\n"
        "• ChatGPT\n"
        "• Gemini\n"
        "• Claude\n"
        "• Grok\n"
        "• DeepSeek\n\n"
        "Send me any message."
    )

    await update.message.reply_text(
        text,
        reply_markup=Keyboards.main_menu()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "/start\n"
        "/help\n"
        "/profile\n"
        "/balance\n"
        "/premium\n"
        "/models"
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = db.get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text("User not found.")
        return

    text = (
        "👤 Profile\n\n"
        f"🆔 ID: {user['user_id']}\n"
        f"👤 Name: {user['first_name']}\n"
        f"💎 Premium: {'Yes' if user['premium'] else 'No'}\n"
        f"💰 Balance: ${user['balance']}\n"
        f"📊 Total Used: {user['total_used']}"
    )

    await update.message.reply_text(text)


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    amount = db.get_balance(update.effective_user.id)

    await update.message.reply_text(
        f"💰 Your Balance: ${amount}"
    )


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "💎 Premium Plans",
        reply_markup=Keyboards.premium_plans()
    )


async def models(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Choose AI Model",
        reply_markup=Keyboards.model_selection()
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text.startswith("/"):
        return

    await update.message.chat.send_action("typing")

    reply = await ai.chat(
        update.effective_user.id,
        text
    )

    await update.message.reply_text(reply)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ==========================
    # MAIN MENU
    # ==========================

    if data == "back_main":

        await query.edit_message_text(
            "🏠 Main Menu",
            reply_markup=Keyboards.main_menu()
        )
        return

    # ==========================
    # MODEL
    # ==========================

    if data.startswith("model_"):

        model = data.replace("model_", "")

        db.update_settings(
            query.from_user.id,
            model=model
        )

        await query.edit_message_text(
            f"✅ AI Model changed to\n\n{model.upper()}",
            reply_markup=Keyboards.model_selection()
        )

        return

    # ==========================
    # HISTORY
    # ==========================

    if data == "history_delete":

        db.clear_history(query.from_user.id)

        await query.edit_message_text(
            "🗑 Chat history deleted.",
            reply_markup=Keyboards.history_menu()
        )

        return

    # ==========================
    # PREMIUM
    # ==========================

    if data == "premium_pro":

        await query.edit_message_text(
            "💎 Pro Plan Selected\n\nProceed to payment."
        )

        return

    if data == "premium_enterprise":

        await query.edit_message_text(
            "🏆 Enterprise Plan Selected\n\nProceed to payment."
        )

        return

    # ==========================
    # SETTINGS
    # ==========================

    if data == "menu_settings":

        await query.edit_message_text(
            "⚙ Settings",
            reply_markup=Keyboards.settings_menu()
        )

        return

    if data == "settings_language":

        await query.answer(
            "Coming Soon!",
            show_alert=True
        )

        return

    if data == "settings_theme":

        await query.answer(
            "Coming Soon!",
            show_alert=True
        )

        return
def main():

    logger.info("Starting AI Telegram Bot...")

    application = Application.builder().token(
        Config.BOT_TOKEN
    ).build()

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("profile", profile)
    )

    application.add_handler(
        CommandHandler("balance", balance)
    )

    application.add_handler(
        CommandHandler("premium", premium)
    )

    application.add_handler(
        CommandHandler("models", models)
    )

    # Chat
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(button_callback)
    )

    # Error Handler
    application.add_error_handler(
        error_handler.handle_error
    )

    logger.info("Bot Started Successfully.")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
