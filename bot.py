import logging

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from config import Config
from handlers import MainHandlers, CHAT
from admin import AdminHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():

    app = Application.builder().token(
        Config.BOT_TOKEN
    ).build()

    handlers = MainHandlers()
    admin = AdminHandler()

    # ==========================
    # USER COMMANDS
    # ==========================

    app.add_handler(
        CommandHandler(
            "start",
            handlers.start
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            handlers.help_command
        )
    )

    app.add_handler(
        CommandHandler(
            "model",
            handlers.model_command
        )
    )

    app.add_handler(
        CommandHandler(
            "profile",
            handlers.profile_command
        )
    )

    app.add_handler(
        CommandHandler(
            "balance",
            handlers.balance_command
        )
    )

    app.add_handler(
        CommandHandler(
            "premium",
            handlers.premium_command
        )
    )

    app.add_handler(
        CommandHandler(
            "history",
            handlers.history_command
        )
    )

    app.add_handler(
        CommandHandler(
            "referral",
            handlers.referral_command
        )
    )

    # ==========================
    # CHAT
    # ==========================

    chat = ConversationHandler(

        entry_points=[
            CommandHandler(
                "chat",
                handlers.chat_command
            )
        ],

        states={

            CHAT: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    handlers.chat_message
                )

            ]

        },

        fallbacks=[

            CommandHandler(
                "cancel",
                handlers.cancel
            )

        ],

        allow_reentry=True

    )

    app.add_handler(chat)

    # ==========================
    # CALLBACKS
    # ==========================

    app.add_handler(
        CallbackQueryHandler(
            handlers.handle_callbacks
        )
    )

    # ==========================
    # ADMIN
    # ==========================

    app.add_handler(
        CommandHandler(
            "admin",
            admin.admin_menu
        )
    )

    app.add_handler(
        CommandHandler(
            "ban",
            admin.ban_user
        )
    )

    app.add_handler(
        CommandHandler(
            "unban",
            admin.unban_user
        )
    )

    app.add_handler(
        CommandHandler(
            "givepremium",
            admin.give_premium
        )
    )

    # ==========================
    # UNKNOWN
    # ==========================

    app.add_handler(

        MessageHandler(

            filters.COMMAND,

            handlers.unknown

        )

    )

    logger.info("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
