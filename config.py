import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    # DeepSeek AI Configuration
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

    # Google Cloud Vision API Configuration
    GOOGLE_CLOUD_CREDENTIALS_PATH = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")

    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = "telegram_math_bot"
    USERS_COLLECTION = "users"
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    HOST = "0.0.0.0"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # production or development
    
    # Timezone Configuration
    TIMEZONE = "Asia/Phnom_Penh"
    
    # Limits
    MAX_ALARMS_PER_USER = 10
    ALARM_RESPONSE_TIMEOUT = 3600  # 1 hour in seconds
    
    # File paths
    TEMP_DIR = "temp"
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_vars = [
            "TELEGRAM_BOT_TOKEN",
            "WEBHOOK_URL",
            "MONGODB_URI",
            "DEEPSEEK_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
