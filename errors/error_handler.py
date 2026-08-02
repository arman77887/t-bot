from telegram import Update
from telegram.ext import ContextTypes
from logger.logger import logger


class ErrorHandler:

    async def handle_error(
        self,
        update: object,
        context: ContextTypes.DEFAULT_TYPE
    ):

        logger.exception(
            f"Exception: {context.error}"
        )

        try:

            if isinstance(update, Update):

                if update.effective_message:

                    await update.effective_message.reply_text(
                        "❌ An internal error occurred.\nPlease try again later."
                    )

        except Exception as e:

            logger.error(
                f"Error while sending error message: {e}"
            )
