"""
Main FastAPI application with improved webhook handling for DigitalOcean deployment
"""

import asyncio
import logging
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import uvicorn

from config import Config
from app.handlers.bot_handlers import bot_handlers
from app.services.alarm_manager import AlarmManager
import app.services.alarm_manager as alarm_module

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

class MathBotApp:
    """Main application class for MathBot"""
    
    def __init__(self):
        self.app = FastAPI(
            title="MathBot Telegram Bot",
            version="2.0.0",
            description="Advanced Mathematical Assistant Telegram Bot",
            docs_url="/docs" if Config.is_development() else None,
            redoc_url="/redoc" if Config.is_development() else None
        )
        self.telegram_app = None
        self.alarm_manager_instance = None
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=Config.ALLOWED_HOSTS,
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        self.app.add_event_handler("startup", self.startup_event)
        self.app.add_event_handler("shutdown", self.shutdown_event)
        
        # Health check endpoints
        self.app.get("/")(self.root)
        self.app.get("/health")(self.health_check)
        
        # Webhook endpoints
        self.app.post("/webhook")(self.webhook)
        self.app.get("/set_webhook")(self.set_webhook)
        self.app.get("/webhook_info")(self.get_webhook_info)
        
        # Statistics endpoint
        self.app.get("/stats")(self.get_bot_stats)
    
    async def setup_telegram_bot(self):
        """Initialize and setup the Telegram bot"""
        try:
            # Create Telegram application
            self.telegram_app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

            # Get and display bot information
            try:
                bot_info = await self.telegram_app.bot.get_me()
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
            self.alarm_manager_instance = AlarmManager(Config.TELEGRAM_BOT_TOKEN)
            alarm_module.alarm_manager = self.alarm_manager_instance

            # Add handlers
            self.telegram_app.add_handler(CommandHandler("start", bot_handlers.start_command))
            self.telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.handle_message))
            self.telegram_app.add_handler(MessageHandler(filters.PHOTO, bot_handlers.handle_photo))
            self.telegram_app.add_handler(CallbackQueryHandler(bot_handlers.handle_callback_query))

            # Initialize the application
            await self.telegram_app.initialize()
            await self.telegram_app.start()

            # Start alarm scheduler
            self.alarm_manager_instance.start_scheduler()

            # Schedule existing alarms
            self.alarm_manager_instance.schedule_all_user_alarms()

            # Set webhook in production mode
            if Config.is_production() and Config.WEBHOOK_URL:
                try:
                    webhook_url = f"{Config.WEBHOOK_URL}/webhook"
                    success = await self.telegram_app.bot.set_webhook(
                        url=webhook_url,
                        secret_token=Config.WEBHOOK_SECRET
                    )
                    if success:
                        logger.info(f"✅ Webhook set successfully to: {webhook_url}")
                    else:
                        logger.error("❌ Failed to set webhook")
                except Exception as e:
                    logger.error(f"❌ Error setting webhook: {e}")

            logger.info("✅ Telegram bot initialized successfully")
            logger.info(f"🚀 Bot is now running and ready to receive messages!")

        except Exception as e:
            logger.error(f"❌ Error setting up Telegram bot: {e}")
            raise

    async def shutdown_telegram_bot(self):
        """Shutdown the Telegram bot"""
        try:
            if self.alarm_manager_instance:
                self.alarm_manager_instance.stop_scheduler()
                logger.info("Alarm scheduler stopped")
            
            if self.telegram_app:
                await self.telegram_app.stop()
                await self.telegram_app.shutdown()
                logger.info("Telegram bot shutdown successfully")
                
        except Exception as e:
            logger.error(f"Error shutting down Telegram bot: {e}")

    async def startup_event(self):
        """FastAPI startup event"""
        logger.info("Starting MathBot application...")
        await self.setup_telegram_bot()
        logger.info("MathBot application started successfully")

    async def shutdown_event(self):
        """FastAPI shutdown event"""
        logger.info("Shutting down MathBot application...")
        await self.shutdown_telegram_bot()
        logger.info("MathBot application shutdown complete")

    async def root(self):
        """Root endpoint for health check"""
        return {
            "status": "ok",
            "message": "MathBot Telegram Bot is running",
            "version": "2.0.0",
            "environment": Config.ENVIRONMENT
        }

    async def health_check(self):
        """Health check endpoint"""
        try:
            # Check if telegram app is running
            if not self.telegram_app:
                raise HTTPException(status_code=503, detail="Telegram bot not initialized")
            
            # Check if alarm manager is running
            if not self.alarm_manager_instance or not self.alarm_manager_instance.scheduler.running:
                raise HTTPException(status_code=503, detail="Alarm scheduler not running")
            
            return {
                "status": "healthy",
                "telegram_bot": "running",
                "alarm_scheduler": "running",
                "scheduled_jobs": len(self.alarm_manager_instance.get_scheduled_jobs()) if self.alarm_manager_instance else 0,
                "environment": Config.ENVIRONMENT
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(status_code=503, detail=str(e))

    def _verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        """Verify webhook signature for security"""
        if not Config.WEBHOOK_SECRET:
            return True  # Skip verification if no secret is set
        
        expected_signature = hmac.new(
            Config.WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)

    async def webhook(self, request: Request, x_telegram_bot_api_secret_token: str = Header(None)):
        """Webhook endpoint for Telegram updates with enhanced security"""
        try:
            if not self.telegram_app:
                raise HTTPException(status_code=503, detail="Telegram bot not initialized")
            
            # Get the update data
            body = await request.body()
            
            # Verify webhook signature if secret token is configured
            if Config.WEBHOOK_SECRET and x_telegram_bot_api_secret_token != Config.WEBHOOK_SECRET:
                logger.warning("Invalid webhook secret token")
                raise HTTPException(status_code=403, detail="Invalid secret token")
            
            # Parse JSON
            try:
                update_data = await request.json()
            except Exception as e:
                logger.error(f"Failed to parse JSON: {e}")
                raise HTTPException(status_code=400, detail="Invalid JSON")
            
            # Create Update object
            update = Update.de_json(update_data, self.telegram_app.bot)
            
            if update:
                # Process the update
                await self.telegram_app.process_update(update)
                logger.debug(f"Processed update: {update.update_id}")
            
            return {"status": "ok"}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def set_webhook(self):
        """Endpoint to set the webhook URL"""
        try:
            if not self.telegram_app:
                raise HTTPException(status_code=503, detail="Telegram bot not initialized")
            
            if not Config.WEBHOOK_URL:
                raise HTTPException(status_code=400, detail="WEBHOOK_URL not configured")
            
            webhook_url = f"{Config.WEBHOOK_URL}/webhook"
            
            # Set the webhook with secret token
            success = await self.telegram_app.bot.set_webhook(
                url=webhook_url,
                secret_token=Config.WEBHOOK_SECRET
            )
            
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

    async def get_webhook_info(self):
        """Get current webhook information"""
        try:
            if not self.telegram_app:
                raise HTTPException(status_code=503, detail="Telegram bot not initialized")
            
            webhook_info = await self.telegram_app.bot.get_webhook_info()
            
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

    async def get_bot_stats(self):
        """Get bot statistics"""
        try:
            from app.models.database import db_manager
            
            # Get total users
            total_users = len(list(db_manager.users.find({})))
            
            # Get users with alarms
            users_with_alarms = len(db_manager.get_all_users_with_alarms())
            
            # Get total alarms
            total_alarms = sum(len(user.get('alarms', [])) for user in db_manager.users.find({}))
            
            # Get scheduled jobs
            scheduled_jobs = len(self.alarm_manager_instance.get_scheduled_jobs()) if self.alarm_manager_instance else 0
            
            return {
                "total_users": total_users,
                "users_with_alarms": users_with_alarms,
                "total_alarms": total_alarms,
                "scheduled_jobs": scheduled_jobs,
                "max_alarms_per_user": Config.MAX_ALARMS_PER_USER,
                "timezone": Config.TIMEZONE,
                "environment": Config.ENVIRONMENT
            }
            
        except Exception as e:
            logger.error(f"Error getting bot stats: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Create the application instance
def create_app() -> FastAPI:
    """Factory function to create the FastAPI app"""
    mathbot = MathBotApp()
    return mathbot.app
