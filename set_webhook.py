#!/usr/bin/env python3
"""
Script to manually set the Telegram webhook for production deployment
"""
import asyncio
import sys
from telegram import Bot
from config import Config

async def set_webhook():
    """Set the webhook for the Telegram bot"""
    try:
        # Validate configuration
        Config.validate()
        
        # Create bot instance
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        # Set webhook URL
        webhook_url = f"{Config.WEBHOOK_URL}/webhook"
        
        print(f"Setting webhook to: {webhook_url}")
        
        # Set the webhook
        success = await bot.set_webhook(url=webhook_url)
        
        if success:
            print("✅ Webhook set successfully!")
            
            # Get webhook info to verify
            webhook_info = await bot.get_webhook_info()
            print(f"📡 Current webhook URL: {webhook_info.url}")
            print(f"📊 Pending updates: {webhook_info.pending_update_count}")
            if webhook_info.last_error_message:
                print(f"⚠️ Last error: {webhook_info.last_error_message}")
        else:
            print("❌ Failed to set webhook")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

async def delete_webhook():
    """Delete the webhook (for development mode)"""
    try:
        # Create bot instance
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        print("Deleting webhook...")
        
        # Delete the webhook
        success = await bot.delete_webhook()
        
        if success:
            print("✅ Webhook deleted successfully!")
        else:
            print("❌ Failed to delete webhook")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

async def get_webhook_info():
    """Get current webhook information"""
    try:
        # Create bot instance
        bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        
        # Get webhook info
        webhook_info = await bot.get_webhook_info()
        
        print("📡 Current Webhook Information:")
        print(f"   URL: {webhook_info.url or 'Not set'}")
        print(f"   Pending updates: {webhook_info.pending_update_count}")
        print(f"   Max connections: {webhook_info.max_connections}")
        print(f"   Has custom certificate: {webhook_info.has_custom_certificate}")
        
        if webhook_info.last_error_date:
            print(f"   Last error date: {webhook_info.last_error_date}")
        if webhook_info.last_error_message:
            print(f"   Last error message: {webhook_info.last_error_message}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python set_webhook.py set     - Set webhook")
        print("  python set_webhook.py delete  - Delete webhook")
        print("  python set_webhook.py info    - Get webhook info")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "set":
        asyncio.run(set_webhook())
    elif command == "delete":
        asyncio.run(delete_webhook())
    elif command == "info":
        asyncio.run(get_webhook_info())
    else:
        print("Invalid command. Use 'set', 'delete', or 'info'")
        sys.exit(1)
