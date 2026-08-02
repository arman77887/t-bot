from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Keyboards:

    @staticmethod
    def main_menu():
        keyboard = [
            [
                InlineKeyboardButton("🤖 Chat", callback_data="menu_chat"),
                InlineKeyboardButton("🎨 Image", callback_data="menu_image")
            ],
            [
                InlineKeyboardButton("🧠 Model", callback_data="menu_model"),
                InlineKeyboardButton("👤 Profile", callback_data="menu_profile")
            ],
            [
                InlineKeyboardButton("💎 Premium", callback_data="menu_premium"),
                InlineKeyboardButton("💰 Balance", callback_data="menu_balance")
            ],
            [
                InlineKeyboardButton("📜 History", callback_data="history_view"),
                InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def model_selection():
        keyboard = [
            [
                InlineKeyboardButton("🤖 ChatGPT", callback_data="model_chatgpt"),
                InlineKeyboardButton("✨ Gemini", callback_data="model_gemini")
            ],
            [
                InlineKeyboardButton("🧠 Claude", callback_data="model_claude"),
                InlineKeyboardButton("⚡ Grok", callback_data="model_grok")
            ],
            [
                InlineKeyboardButton("🚀 DeepSeek", callback_data="model_deepseek")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def premium_plans():
        keyboard = [
            [
                InlineKeyboardButton("💎 Pro", callback_data="premium_pro")
            ],
            [
                InlineKeyboardButton("🏆 Enterprise", callback_data="premium_enterprise")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def settings_menu():
        keyboard = [
            [
                InlineKeyboardButton("🌐 Language", callback_data="settings_language")
            ],
            [
                InlineKeyboardButton("🎨 Theme", callback_data="settings_theme")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def history_menu():
        keyboard = [
            [
                InlineKeyboardButton("🗑 Delete History", callback_data="history_delete")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
