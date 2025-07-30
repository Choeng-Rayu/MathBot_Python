import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")  # For webhook security

    # AI Configuration
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

    # Google Gemini AI Configuration
    GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
    GOOGLE_GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    # AI Model Selection (gemini, deepseek, or auto)
    AI_MODEL = os.getenv("AI_MODEL", "auto")  # auto will try gemini first, then deepseek

    # Google Cloud Vision API Configuration
    GOOGLE_CLOUD_CREDENTIALS_PATH = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")
    GOOGLE_CLOUD_CREDENTIALS_JSON = os.getenv("GOOGLE_CLOUD_CREDENTIALS_JSON")

    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = "telegram_math_bot"
    USERS_COLLECTION = "users"

    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # production or development

    # DigitalOcean App Platform specific
    APP_URL = os.getenv("APP_URL")  # DigitalOcean app URL

    # Security Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

    # Timezone Configuration
    TIMEZONE = "Asia/Phnom_Penh"

    # Limits
    MAX_ALARMS_PER_USER = 10
    ALARM_RESPONSE_TIMEOUT = 3600  # 1 hour in seconds

    # File paths
    TEMP_DIR = "temp"

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            "TELEGRAM_BOT_TOKEN",
            "MONGODB_URI"
        ]

        # At least one AI API key is required
        ai_keys = [cls.DEEPSEEK_API_KEY, cls.GOOGLE_GEMINI_API_KEY]
        if not any(ai_keys):
            required_vars.extend(["DEEPSEEK_API_KEY or GOOGLE_GEMINI_API_KEY"])

        # WEBHOOK_URL is only required in production
        if cls.ENVIRONMENT == "production":
            required_vars.append("WEBHOOK_URL")

        missing_vars = []
        for var in required_vars:
            if "or" in var:  # Handle AI key requirement
                continue
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # Log configuration status
        logger.info(f"Environment: {cls.ENVIRONMENT}")
        logger.info(f"Port: {cls.PORT}")
        logger.info(f"Host: {cls.HOST}")
        logger.info(f"AI Model: {cls.AI_MODEL}")

        # Log available AI services
        if cls.DEEPSEEK_API_KEY:
            logger.info("✅ DeepSeek AI available")
        if cls.GOOGLE_GEMINI_API_KEY:
            logger.info("✅ Google Gemini AI available")

        if cls.WEBHOOK_URL:
            logger.info(f"Webhook URL: {cls.WEBHOOK_URL}")

        return True

    @classmethod
    def is_production(cls):
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() == "production"

    @classmethod
    def is_development(cls):
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() == "development"
