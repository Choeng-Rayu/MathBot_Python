#!/usr/bin/env python3
"""
Main entry point for MathBot Telegram Bot
Optimized for DigitalOcean App Platform deployment
"""

import os
import sys
import logging
import uvicorn

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from app.core.app import create_app

# Create the app instance for uvicorn reload functionality
app = create_app()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        # Validate configuration
        Config.validate()
        logger.info("Configuration validated successfully")

        # Use the global app instance

        # Run the application
        logger.info(f"Starting MathBot on {Config.HOST}:{Config.PORT}")
        logger.info(f"Environment: {Config.ENVIRONMENT}")

        if Config.is_development():
            # Development mode with reload
            uvicorn.run(
                "main:app",  # Import string for reload functionality
                host=Config.HOST,
                port=Config.PORT,
                reload=True,
                log_level=Config.LOG_LEVEL.lower()
            )
        else:
            # Production mode without reload
            uvicorn.run(
                app,
                host=Config.HOST,
                port=Config.PORT,
                reload=False,
                log_level=Config.LOG_LEVEL.lower()
            )

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
