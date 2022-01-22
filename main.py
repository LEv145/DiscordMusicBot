from pathlib import Path

from config import BOT_TOKEN

from lightbulb import BotApp
from loguru import logger


logger.add(Path("log/main.log"), rotation="500 MB")

bot = BotApp(token=BOT_TOKEN, prefix="!")

bot.load_extensions("extensions.commands.music")


bot.run()
