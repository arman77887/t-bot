from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from telegram.constants import ParseMode

from database import Database
from config import Config
from keyboards import Keyboards
from logger.logger import logger

from ai.gemini_ai import GeminiHandler
from ai.openai_ai import OpenAIHandler
from ai.claude_ai import ClaudeHandler
from ai.deepseek_ai import DeepSeekHandler
from ai.grok_ai import GrokHandler
from ai.memory import ConversationMemory

from services.history import HistoryHandler
from services.referral import ReferralHandler

from admin import AdminHandler

CHAT = 1


class MainHandlers:

    def __init__(self):

        self.db = Database()

        self.memory = ConversationMemory(self.db)

        self.history = HistoryHandler()

        self.referral = ReferralHandler()

        self.admin = AdminHandler()

        self.gemini = GeminiHandler()
        self.openai = OpenAIHandler()
        self.claude = ClaudeHandler()
        self.deepseek = DeepSeekHandler()
        self.grok = GrokHandler()

        self.default_model = Config.DEFAULT_MODEL

    async def start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        user = update.effective_user

        self.db.register_user(
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            user.language_code,
        )

        text = f"""
👋 Welcome {user.first_name}

🤖 Professional AI Telegram Bot

Available Models

• Gemini
• ChatGPT
• Claude
• DeepSeek
• Grok

Use /chat to start chatting.
"""

        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=Keyboards.main_menu()
        )

    async def help_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        text = """
📚 Commands

/start
/help
/chat
/model
/profile
/balance
/history
/premium
/referral
/settings
"""

        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN
        )

    async def chat_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        user_id = update.effective_user.id

        if self.db.is_banned(user_id):
            await update.message.reply_text("🚫 You are banned.")
            return ConversationHandler.END

        used = self.db.get_daily_usage(user_id)

        if self.db.is_premium(user_id):
            limit = Config.PREMIUM_DAILY_LIMIT
        else:
            limit = Config.DAILY_FREE_LIMIT

        if used >= limit:
            await update.message.reply_text(
                f"❌ Daily limit reached.\n\nUsed: {used}/{limit}"
            )
            return ConversationHandler.END

        model = context.user_data.get(
            "model",
            Config.DEFAULT_MODEL
        )

        await update.message.reply_text(
            f"🤖 Current Model: {model}\n\nSend your message."
        )

        return CHAT

    async def chat_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        user_id = update.effective_user.id

        prompt = update.message.text

        model = context.user_data.get(
            "model",
            Config.DEFAULT_MODEL
        )

        await update.message.chat.send_action("typing")

        try:

            if model == "gemini":

                response = await self.gemini.chat([
                    {
                        "role": "user",
                        "content": prompt
                    }
                ])

            elif model == "chatgpt":

                response = await self.openai.chat([
                    {
                        "role": "user",
                        "content": prompt
                    }
                ])

            elif model == "claude":

                response = await self.claude.chat([
                    {
                        "role": "user",
                        "content": prompt
                    }
                ])

            elif model == "deepseek":

                response = await self.deepseek.chat([
                    {
                        "role": "user",
                        "content": prompt
                    }
                ])

            elif model == "grok":

                response = await self.grok.chat([
                    {
                        "role": "user",
                        "content": prompt
                    }
                ])

            else:

                response = {
                    "error": "Unknown AI model"
                }

            if "error" in response:

                await update.message.reply_text(
                    f"❌ {response['error']}"
                )

            else:

                await update.message.reply_text(
                    response["response"]
                )

                self.db.save_history(
                    user_id,
                    "user",
                    prompt,
                    model
                )

                self.db.save_history(
                    user_id,
                    "assistant",
                    response["response"],
                    model
                )

                self.db.update_user_usage(user_id)

        except Exception as e:

            logger.error(f"Chat error: {e}")

            await update.message.reply_text(
                "❌ Something went wrong."
            )

        return ConversationHandler.END

    async def model_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        await update.message.reply_text(
            "🤖 Select AI Model",
            reply_markup=Keyboards.model_selection()
        )

    async def profile_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        user = self.db.get_user(
            update.effective_user.id
        )

        premium = "✅ Yes" if user["premium"] else "❌ No"

        text = f"""
👤 Profile

🆔 ID: {user['user_id']}

👤 Name: {user['first_name']}

⭐ Premium: {premium}

💰 Balance: ${user['balance']}

📊 Daily Usage:
{user['daily_used']}/{Config.DAILY_FREE_LIMIT}
"""

        await update.message.reply_text(text)

    async def balance_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        balance = self.db.get_balance(
            update.effective_user.id
        )

        await update.message.reply_text(
            f"💰 Balance: ${balance}"
        )

    async def premium_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        text = f"""
⭐ Premium

Price:
{Config.PREMIUM_PRICE} {Config.PREMIUM_CURRENCY}

Benefits

✅ Unlimited Chat

✅ All AI Models

✅ Faster Response

✅ Future Updates
"""

        await update.message.reply_text(
            text,
            reply_markup=Keyboards.premium_plans()
        )

    async def history_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        history = self.db.get_history(
            update.effective_user.id,
            10
        )

        if not history:

            await update.message.reply_text(
                "No history found."
            )

            return

        text = "📚 Chat History\n\n"

        for item in history:

            msg = item["message"][:50]

            text += f"• {msg}\n"

        await update.message.reply_text(
            text,
            reply_markup=Keyboards.history_menu()
        )

    async def referral_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        stats = self.db.get_referral_stats(
            update.effective_user.id
        )

        bot = await context.bot.get_me()

        link = (
            f"https://t.me/{bot.username}"
            f"?start={stats['referral_code']}"
        )

        text = f"""
🎁 Referral

Code:
{stats['referral_code']}

Users:
{stats['total_referrals']}

Earned:
${stats['total_earned']}

Invite Link

{link}
"""

        await update.message.reply_text(text)

    async def handle_callbacks(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        query = update.callback_query

        await query.answer()

        data = query.data

        # ======================
        # MODEL SELECT
        # ======================

        if data.startswith("model_"):

            model = data.replace("model_", "")

            if model not in Config.AVAILABLE_MODELS:

                await query.edit_message_text(
                    "❌ Invalid model."
                )

                return

            if not Config.AVAILABLE_MODELS[model]["enabled"]:

                await query.edit_message_text(
                    f"❌ {model} API is not configured."
                )

                return

            context.user_data["model"] = model

            self.db.set_model(
                query.from_user.id,
                model
            )

            await query.edit_message_text(
                f"✅ Model changed to {Config.AVAILABLE_MODELS[model]['name']}"
            )

            return

        # ======================
        # MAIN MENU
        # ======================

        if data == "back_main":

            await query.edit_message_text(
                "🏠 Main Menu",
                reply_markup=Keyboards.main_menu()
            )

            return

        # ======================
        # SETTINGS
        # ======================

        if data == "menu_settings":

            await query.edit_message_text(
                "⚙ Settings",
                reply_markup=Keyboards.settings_menu()
            )

            return

        if data == "settings_language":

            await query.edit_message_text(
                "🌐 Language feature coming soon."
            )

            return

        if data == "settings_theme":

            await query.edit_message_text(
                "🎨 Theme feature coming soon."
            )

            return

        # ======================
        # PREMIUM
        # ======================

        if data == "premium_buy":

            await query.edit_message_text(
                "💳 Payment system coming soon."
            )

            return

        # ======================
        # HISTORY
        # ======================

        if data == "history_delete":

            self.db.clear_history(
                query.from_user.id
            )

            await query.edit_message_text(
                "✅ History deleted."
            )

            return

        # ======================
        # ADMIN
        # ======================

        if data.startswith("admin_"):

            await self.admin.handle_admin_callbacks(
                update,
                context
            )

            return

        await query.edit_message_text(
            "Unknown action."
        )

    async def unknown(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        await update.message.reply_text(
            "❌ Unknown command.\nUse /help"
        )
