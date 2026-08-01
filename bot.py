import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from config import Config
from handlers import start, help_command, chat_handler
from admin import admin_panel
from errors.error_handler import error_handler
from logger.logger import setup_logger


logger = setup_logger()


async def main():

    app = Application.builder().token(
        Config.BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("admin", admin_panel)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat_handler
        )
    )


    app.add_error_handler(
        error_handler
    )


    logger.info(
        "Bot started successfully"
    )


    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
