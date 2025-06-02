import asyncio
import logging
from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import uvicorn
from config import Config
from bot_handlers import bot_handlers
from alarm_manager import AlarmManager
import alarm_manager as alarm_module

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Validate configuration
try:
    Config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    exit(1)

# Initialize FastAPI app
app = FastAPI(title="MathBot Telegram Bot", version="1.0.0")

# Initialize Telegram bot application
telegram_app = None
alarm_manager_instance = None

async def setup_telegram_bot():
    """Initialize and setup the Telegram bot"""
    global telegram_app, alarm_manager_instance

    try:
        # Create Telegram application
        telegram_app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

        # Get and display bot information
        try:
            bot_info = await telegram_app.bot.get_me()
            logger.info("=" * 60)
            logger.info("🤖 BOT INFORMATION")
            logger.info("=" * 60)
            logger.info(f"📛 Bot Name: {bot_info.first_name}")
            logger.info(f"👤 Username: @{bot_info.username}")
            logger.info(f"🆔 Bot ID: {bot_info.id}")
            logger.info(f"🔗 Bot Link: https://t.me/{bot_info.username}")
            logger.info(f"📨 Can join groups: {bot_info.can_join_groups}")
            logger.info(f"🔒 Can read all group messages: {bot_info.can_read_all_group_messages}")
            logger.info(f"⚙️ Supports inline queries: {bot_info.supports_inline_queries}")

            # Display creator information
            logger.info("=" * 60)
            logger.info("👨‍💻 CREATOR INFORMATION")
            logger.info("=" * 60)
            logger.info("📛 Creator: Choeng Rayu")
            logger.info("📧 Email: choengrayu307@gmail.com")
            logger.info("📱 Telegram: @President_Alein")
            logger.info("🌐 Website: https://rayuchoeng-profolio-website.netlify.app/")
            logger.info("🎯 Purpose: Free mathematical assistance for users")
            logger.info("=" * 60)

        except Exception as e:
            logger.warning(f"Could not fetch bot info: {e}")

        # Initialize alarm manager
        alarm_manager_instance = AlarmManager(Config.TELEGRAM_BOT_TOKEN)
        alarm_module.alarm_manager = alarm_manager_instance

        # Add handlers
        telegram_app.add_handler(CommandHandler("start", bot_handlers.start_command))
        telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.handle_message))
        telegram_app.add_handler(CallbackQueryHandler(bot_handlers.handle_callback_query))

        # Initialize the application
        await telegram_app.initialize()
        await telegram_app.start()

        # Start alarm scheduler
        alarm_manager_instance.start_scheduler()

        # Schedule existing alarms
        alarm_manager_instance.schedule_all_user_alarms()

        logger.info("✅ Telegram bot initialized successfully")
        logger.info(f"🚀 Bot is now running and ready to receive messages!")

    except Exception as e:
        logger.error(f"❌ Error setting up Telegram bot: {e}")
        raise

async def shutdown_telegram_bot():
    """Shutdown the Telegram bot"""
    global telegram_app, alarm_manager_instance
    
    try:
        if alarm_manager_instance:
            alarm_manager_instance.stop_scheduler()
            logger.info("Alarm scheduler stopped")
        
        if telegram_app:
            await telegram_app.stop()
            await telegram_app.shutdown()
            logger.info("Telegram bot shutdown successfully")
            
    except Exception as e:
        logger.error(f"Error shutting down Telegram bot: {e}")

@app.on_event("startup")
async def startup_event():
    """FastAPI startup event"""
    logger.info("Starting MathBot application...")
    await setup_telegram_bot()
    logger.info("MathBot application started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """FastAPI shutdown event"""
    logger.info("Shutting down MathBot application...")
    await shutdown_telegram_bot()
    logger.info("MathBot application shutdown complete")

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {
        "status": "ok",
        "message": "MathBot Telegram Bot is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if telegram app is running
        if not telegram_app:
            raise HTTPException(status_code=503, detail="Telegram bot not initialized")
        
        # Check if alarm manager is running
        if not alarm_manager_instance or not alarm_manager_instance.scheduler.running:
            raise HTTPException(status_code=503, detail="Alarm scheduler not running")
        
        return {
            "status": "healthy",
            "telegram_bot": "running",
            "alarm_scheduler": "running",
            "scheduled_jobs": len(alarm_manager_instance.get_scheduled_jobs()) if alarm_manager_instance else 0
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))

@app.post("/webhook")
async def webhook(request: Request):
    """Webhook endpoint for Telegram updates"""
    try:
        if not telegram_app:
            raise HTTPException(status_code=503, detail="Telegram bot not initialized")
        
        # Get the update data
        update_data = await request.json()
        
        # Create Update object
        update = Update.de_json(update_data, telegram_app.bot)
        
        if update:
            # Process the update
            await telegram_app.process_update(update)
            logger.debug(f"Processed update: {update.update_id}")
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/set_webhook")
async def set_webhook():
    """Endpoint to set the webhook URL"""
    try:
        if not telegram_app:
            raise HTTPException(status_code=503, detail="Telegram bot not initialized")
        
        webhook_url = f"{Config.WEBHOOK_URL}/webhook"
        
        # Set the webhook
        success = await telegram_app.bot.set_webhook(url=webhook_url)
        
        if success:
            logger.info(f"Webhook set successfully to: {webhook_url}")
            return {
                "status": "success",
                "message": f"Webhook set to {webhook_url}"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to set webhook")
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/webhook_info")
async def get_webhook_info():
    """Get current webhook information"""
    try:
        if not telegram_app:
            raise HTTPException(status_code=503, detail="Telegram bot not initialized")
        
        webhook_info = await telegram_app.bot.get_webhook_info()
        
        return {
            "url": webhook_info.url,
            "has_custom_certificate": webhook_info.has_custom_certificate,
            "pending_update_count": webhook_info.pending_update_count,
            "last_error_date": webhook_info.last_error_date,
            "last_error_message": webhook_info.last_error_message,
            "max_connections": webhook_info.max_connections,
            "allowed_updates": webhook_info.allowed_updates
        }
        
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_bot_stats():
    """Get bot statistics"""
    try:
        from database import db_manager
        
        # Get total users
        total_users = len(list(db_manager.users.find({})))
        
        # Get users with alarms
        users_with_alarms = len(db_manager.get_all_users_with_alarms())
        
        # Get total alarms
        total_alarms = sum(len(user.get('alarms', [])) for user in db_manager.users.find({}))
        
        # Get scheduled jobs
        scheduled_jobs = len(alarm_manager_instance.get_scheduled_jobs()) if alarm_manager_instance else 0
        
        return {
            "total_users": total_users,
            "users_with_alarms": users_with_alarms,
            "total_alarms": total_alarms,
            "scheduled_jobs": scheduled_jobs,
            "max_alarms_per_user": Config.MAX_ALARMS_PER_USER,
            "timezone": Config.TIMEZONE
        }
        
    except Exception as e:
        logger.error(f"Error getting bot stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=False,  # Set to True for development
        log_level="info"
    )
