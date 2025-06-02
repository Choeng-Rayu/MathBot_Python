#!/usr/bin/env python3
"""
Simple startup script for MathBot
"""

import os
import sys
import asyncio
from config import Config

def check_environment():
    """Check if all required environment variables are set"""
    try:
        Config.validate()
        print("✅ Environment configuration is valid")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set:")
        print("- TELEGRAM_BOT_TOKEN")
        print("- WEBHOOK_URL") 
        print("- MONGODB_URI")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    # Map package names to their import names
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'python-telegram-bot': 'telegram',
        'pymongo': 'pymongo',
        'python-dotenv': 'dotenv',
        'sympy': 'sympy',
        'matplotlib': 'matplotlib',
        'reportlab': 'reportlab',
        'apscheduler': 'apscheduler',
        'pytz': 'pytz',
        'numpy': 'numpy',
        'requests': 'requests'
    }

    missing_packages = []

    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name}")
            missing_packages.append(package_name)

    if missing_packages:
        print(f"\n❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False

    print("\n✅ All required packages are installed")
    return True

async def get_bot_info():
    """Get bot information from Telegram API"""
    try:
        from telegram import Bot
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)

        # Get bot information
        bot_info = await bot.get_me()

        print("🤖 Bot Information:")
        print(f"   📛 Name: {bot_info.first_name}")
        print(f"   👤 Username: @{bot_info.username}")
        print(f"   🆔 Bot ID: {bot_info.id}")
        print(f"   🔗 Bot Link: https://t.me/{bot_info.username}")

        if bot_info.description:
            print(f"   📝 Description: {bot_info.description}")

        # Check if bot can receive messages
        print(f"   📨 Can join groups: {bot_info.can_join_groups}")
        print(f"   🔒 Can read all group messages: {bot_info.can_read_all_group_messages}")
        print(f"   ⚙️ Supports inline queries: {bot_info.supports_inline_queries}")

        return True

    except Exception as e:
        print(f"⚠️ Could not fetch bot info: {e}")
        print("   (Bot will still work, but check your TELEGRAM_BOT_TOKEN)")
        return False

async def start_polling_mode():
    """Start bot in polling mode for development"""
    try:
        from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
        from bot_handlers import bot_handlers
        from alarm_manager import AlarmManager
        import alarm_manager as alarm_module

        print("🔄 Starting bot in DEVELOPMENT mode (polling)...")

        # Create Telegram application
        app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

        # Get and display bot information
        try:
            bot_info = await app.bot.get_me()
            print("🤖 Bot Information:")
            print(f"   📛 Name: {bot_info.first_name}")
            print(f"   👤 Username: @{bot_info.username}")
            print(f"   🆔 Bot ID: {bot_info.id}")
            print(f"   🔗 Bot Link: https://t.me/{bot_info.username}")
            print("=" * 50)
        except Exception as e:
            print(f"⚠️ Could not fetch bot info: {e}")

        # Initialize alarm manager
        alarm_manager_instance = AlarmManager(Config.TELEGRAM_BOT_TOKEN)
        alarm_module.alarm_manager = alarm_manager_instance

        # Add handlers
        app.add_handler(CommandHandler("start", bot_handlers.start_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.handle_message))
        app.add_handler(CallbackQueryHandler(bot_handlers.handle_callback_query))

        # Start alarm scheduler
        alarm_manager_instance.start_scheduler()
        alarm_manager_instance.schedule_all_user_alarms()

        # Start polling
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

        print("✅ Bot successfully launched!")
        print(f"🤖 Bot @{bot_info.username} is running...")
        print("📱 You can now interact with the bot on Telegram")
        print("🔍 Debug mode: Enabled")
        print("🛑 Press Ctrl+C to stop the bot")

        # Keep the bot running
        import signal
        import asyncio

        # Handle shutdown gracefully
        def signal_handler(signum, frame):
            print("\n� Shutting down bot...")
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("🛑 Bot stopped by user")
        finally:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()
            alarm_manager_instance.stop_scheduler()
            print("✅ Bot shutdown complete")

    except Exception as e:
        print(f"❌ Failed to launch bot: {e}")
        print("� Check your TELEGRAM_BOT_TOKEN and internet connection")
        sys.exit(1)

def start_webhook_mode():
    """Start bot in webhook mode for production"""
    try:
        print("🌐 Starting bot in PRODUCTION mode (webhook)...")
        print(f"� Webhook URL: {Config.WEBHOOK_URL}")
        print(f"📡 Port: {Config.PORT}")
        print("=" * 50)

        import uvicorn
        from main import app

        uvicorn.run(
            app,
            host=Config.HOST,
            port=Config.PORT,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting webhook mode: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🤖 Starting MathBot Telegram Bot...")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Check environment
    if not check_environment():
        sys.exit(1)

    # Create temp directory if it doesn't exist
    os.makedirs(Config.TEMP_DIR, exist_ok=True)
    print(f"✅ Temporary directory created: {Config.TEMP_DIR}")

    # Determine mode based on environment
    is_production = os.getenv('NODE_ENV') == 'production' or os.getenv('ENVIRONMENT') == 'production'

    # You can also force polling mode by setting FORCE_POLLING=true
    force_polling = os.getenv('FORCE_POLLING', '').lower() == 'true'

    if force_polling:
        print("🔧 FORCE_POLLING enabled - using polling mode")
        is_production = False

    try:
        if is_production:
            # Production mode: Use webhook
            start_webhook_mode()
        else:
            # Development mode: Use polling
            import asyncio
            asyncio.run(start_polling_mode())

    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
