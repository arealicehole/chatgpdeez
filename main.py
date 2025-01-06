import asyncio
import logging
from bot import setup_bot
from config import DISCORD_TOKEN, setup_logging

setup_logging()
logger = logging.getLogger(__name__)

async def main():
    bot = setup_bot()
    try:
        logger.info("Starting bot...")
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}", exc_info=True)
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
