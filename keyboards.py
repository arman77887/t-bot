from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Keyboards:

    @staticmethod
    def main_menu():
        keyboard = [
            [
                InlineKeyboardButton("💬 Chat", callback_data="menu_chat"),
                InlineKeyboardButton("🤖 Models", callback_data="menu_models")
            ],
            [
                InlineKeyboardButton("👤 Profile", callback_data="menu_profile"),
                InlineKeyboardButton("💰 Balance", callback_data="menu_balance")
            ],
            [
                InlineKeyboardButton("⭐ Premium", callback_data="menu_premium"),
                InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
            ],
            [
                InlineKeyboardButton("📚 History", callback_data="menu_history"),
                InlineKeyboardButton("🎁 Referral", callback_data="menu_referral")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def model_selection():
        keyboard = [
            [InlineKeyboardButton("🧠 Gemini", callback_data="model_gemini")],
            [InlineKeyboardButton("🤖 ChatGPT", callback_data="model_chatgpt")],
            [InlineKeyboardButton("🟣 Claude", callback_data="model_claude")],
            [InlineKeyboardButton("🔵 DeepSeek", callback_data="model_deepseek")],
            [InlineKeyboardButton("❌ Grok", callback_data="model_grok")],
            [InlineKeyboardButton("⬅ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def premium_plans():
        keyboard = [
            [InlineKeyboardButton("⭐ Buy Premium", callback_data="premium_buy")],
            [InlineKeyboardButton("⬅ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def settings_menu():
        keyboard = [
            [InlineKeyboardButton("🌐 Language", callback_data="settings_language")],
            [InlineKeyboardButton("🎨 Theme", callback_data="settings_theme")],
            [InlineKeyboardButton("⬅ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def history_menu():
        keyboard = [
            [InlineKeyboardButton("🗑 Delete History", callback_data="history_delete")],
            [InlineKeyboardButton("⬅ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def admin_menu():
        keyboard = [
            [InlineKeyboardButton("👥 Users", callback_data="admin_users")],
            [InlineKeyboardButton("⭐ Premium", callback_data="admin_premium")],
            [InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban")],
            [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
            [InlineKeyboardButton("⬅ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
