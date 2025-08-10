# Cara Install Bot Jabber di Android

## Download Manual (Copy-Paste)

Jika tidak bisa download langsung, copy kode ini:

### 1. Buat file `main.py`:
```python
#!/usr/bin/env python3
"""
Main entry point for the Jabber/XMPP bot.
"""

import argparse
import asyncio
import logging
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
    
    try:
        # Create and run the bot
        bot = JabberBot(args.config)
        logger.info("Starting Jabber bot...")
        
        # Connect and run the bot
        bot.connect()
        
        # Keep the bot running
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

def main():
    """Main function to run the Jabber bot."""
    asyncio.run(main_async())

if __name__ == '__main__':
    main()
```

### 2. Install di Android:
1. Install Termux dari Google Play Store
2. Buka Termux, ketik:
```bash
pkg update
pkg install python
pip install slixmpp configparser pytz
```

3. Buat folder project:
```bash
mkdir jabberbot
cd jabberbot
```

4. Copy semua file Python ke folder ini
5. Edit config.ini dengan kredensial XMPP Anda
6. Jalankan: `python main.py --debug`

## Cara Mudah: Gunakan Browser
1. Buka https://replit.com di browser Android
2. Login ke akun Anda
3. Buka project bot ini
4. Klik Download/Export
5. File akan terdownload sebagai ZIP

Bot akan berjalan sempurna di HP Android via Termux!