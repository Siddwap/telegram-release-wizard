#!/usr/bin/env python3
"""
Simple runner script for the Telegram bot and Flask app.
"""
import asyncio
import sys
import logging
import signal
from bot import TelegramBot
from config import BotConfig
from threading import Thread
from app import app

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from aiohttp and other libraries
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.getLogger('telethon').setLevel(logging.WARNING)

async def start_bot():
    """Start the Telegram bot"""
    logger = logging.getLogger(__name__)
    try:
        # Load and validate configuration
        config = BotConfig.from_env()
        config.validate()
        
        logger.info("Starting Telegram GitHub Release Uploader Bot...")
        logger.info(f"Target repository: {config.github_repo}")
        logger.info(f"Release tag: {config.github_release_tag}")
        
        # Start the bot
        bot = TelegramBot()
        await bot.start()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

def run_flask():
    """Start the Flask app"""
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    setup_logging()
    
    # Start Flask app in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Bot stopped by user")
        sys.exit(0)
