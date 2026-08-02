# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

# .env ফাইলের পাথ নির্ধারণ
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """
    সমস্ত কনফিগারেশন ভেরিয়েবল এখানে সংরক্ষণ করা হয়
    """
    
    # ========================
    # TELEGRAM BOT
    # ========================
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
    
    # ========================
    # AI API KEYS
    # ========================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    
    # ========================
    # DATABASE
    # ========================
    DATABASE_NAME = os.getenv("DATABASE_NAME", "database/bot.db")
    
    # ========================
    # AI MODELS
    # ========================
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini")
    
    # উপলব্ধ মডেলগুলির তালিকা
    AVAILABLE_MODELS = {
        "gemini": {
            "name": "Gemini",
            "enabled": bool(GEMINI_API_KEY),
            "handler": "GeminiHandler"
        },
        "chatgpt": {
            "name": "ChatGPT",
            "enabled": bool(OPENAI_API_KEY),
            "handler": "OpenAIHandler"
        },
        "claude": {
            "name": "Claude",
            "enabled": bool(CLAUDE_API_KEY),
            "handler": "ClaudeHandler"
        },
        "deepseek": {
            "name": "DeepSeek",
            "enabled": bool(DEEPSEEK_API_KEY),
            "handler": "DeepSeekHandler"
        },
        "grok": {
            "name": "Grok",
            "enabled": bool(GROK_API_KEY),
            "handler": "GrokHandler"
        }
    }
    
    # ========================
    # USER LIMITS
    # ========================
    DAILY_FREE_LIMIT = int(os.getenv("DAILY_FREE_LIMIT", 10))
    PREMIUM_DAILY_LIMIT = int(os.getenv("PREMIUM_DAILY_LIMIT", 100))
    
    # ========================
    # PREMIUM
    # ========================
    PREMIUM_PRICE = float(os.getenv("PREMIUM_PRICE", 9.99))
    PREMIUM_CURRENCY = os.getenv("PREMIUM_CURRENCY", "USD")
    
    # ========================
    # LOGGING
    # ========================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")
    
    # ========================
    # VALIDATION
    # ========================
    @classmethod
    def validate(cls):
        """
        কনফিগারেশন ভ্যালিডেট করে - প্রয়োজনীয় ভেরিয়েবল চেক করে
        """
        errors = []
        warnings = []
        
        # বট টোকেন চেক
        if not cls.BOT_TOKEN:
            errors.append("❌ BOT_TOKEN is not set in .env file")
        
        # API Keys চেক
        enabled_models = cls.get_enabled_models()
        if not enabled_models:
            errors.append("❌ No AI API keys found. At least one AI service must be configured.")
        else:
            warnings.append(f"⚠️  Enabled models: {', '.join(enabled_models.keys())}")
        
        # অ্যাডমিন আইডি চেক
        if not cls.ADMIN_IDS:
            warnings.append("⚠️  No ADMIN_IDS configured")
        
        if errors:
            raise ValueError("\n".join(errors))
        
        if warnings:
            print("\n".join(warnings))
        
        return True
    
    @classmethod
    def get_enabled_models(cls):
        """
        শুধুমাত্র সক্রিয় মডেলগুলির তালিকা রিটার্ন করে
        """
        return {
            key: value 
            for key, value in cls.AVAILABLE_MODELS.items() 
            if value["enabled"]
        }
    
    @classmethod
    def get_model_handler(cls, model_name):
        """
        নির্দিষ্ট মডেলের জন্য হ্যান্ডলার ক্লাসের নাম রিটার্ন করে
        """
        if model_name in cls.AVAILABLE_MODELS:
            return cls.AVAILABLE_MODELS[model_name].get("handler")
        return None
    
    @classmethod
    def is_admin(cls, user_id):
        """
        চেক করে ইউজার অ্যাডমিন কিনা
        """
        return user_id in cls.ADMIN_IDS

# কনফিগারেশন ভ্যালিডেট করুন (যদি প্রয়োজন হয়)
if __name__ == "__main__":
    try:
        Config.validate()
        print("\n✅ Configuration is valid!")
        print(f"🤖 Bot Token: {Config.BOT_TOKEN[:10]}...{Config.BOT_TOKEN[-5:]}")
        print(f"👥 Admins: {Config.ADMIN_IDS}")
        print(f"📊 Enabled Models: {list(Config.get_enabled_models().keys())}")
    except ValueError as e:
        print(f"\n❌ {e}")
