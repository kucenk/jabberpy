#!/usr/bin/env python3
"""
Main entry point for the Jabber/XMPP bot.
"""

import argparse
import asyncio
import logging
import signal
import sys
from jabberbot import JabberBot

def setup_logging(debug=False):
    """Setup logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('jabberbot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

async def main_async():
    """Async main function to run the Jabber bot."""
    parser = argparse.ArgumentParser(description='Python Jabber/XMPP Bot')
    parser.add_argument('-c', '--config', default='config.ini',
                       help='Configuration file path (default: config.ini)')
    parser.add_argument('-d', '--debug', action='store_true',
                       help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)
    
    bot = None
    shutdown_event = asyncio.Event()
    
    def signal_handler():
        logger.info("Received shutdown signal")
        shutdown_event.set()
    
    # Setup signal handlers for graceful shutdown
    for sig in [signal.SIGTERM, signal.SIGINT]:
        asyncio.get_event_loop().add_signal_handler(sig, signal_handler)
    
    try:
        # Create and run the bot
        bot = JabberBot(args.config)
        logger.info("Starting Jabber bot...")
        
        # Connect and run the bot
        bot.connect()
        
        # Keep the bot running until shutdown signal
        await shutdown_event.wait()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup when stopping
        if bot:
            if hasattr(bot, 'scheduler') and bot.scheduler:
                await bot.scheduler.stop()
            bot.disconnect()
            logger.info("Bot shutdown complete")

def main():
    """Main function to run the Jabber bot."""
    asyncio.run(main_async())

if __name__ == '__main__':
    main()
