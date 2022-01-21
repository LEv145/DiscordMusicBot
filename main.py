from pathlib import Path

from config import BOT_TOKEN

import hikari
from lightbulb import BotApp
from loguru import logger


logger.add(Path("log/main.log"), rotation="500 MB")

bot = BotApp(token=BOT_TOKEN)


@bot.listen(hikari.ShardReadyEvent)
async def on_ready(event: hikari.ShardReadyEvent) -> None:
    logger.info(f"We have logged in as {event.my_user}")


bot.run()
