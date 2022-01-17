import sys
from pathlib import Path
import asyncio

from bot import Bot

from loguru import logger


async def main():
    logger.add(sys.stdout)
    logger.add("main.log", rotation="500 MB")

    bot = Bot()
    bot.run()


asyncio.run(main())
