from pathlib import Path

from hikari import Intents
from loguru import logger

from config import BOT_TOKEN
from bot import BaseBot


EXTENSIONS = (
    "extensions.commands.test_extension",
)

logger.add(Path("log/main.log"), rotation="500 MB")


bot = BaseBot(
    token=BOT_TOKEN,
    owner_ids=(501089151089770517,),
    intents=Intents.NONE,
    default_enabled_guilds=(867344761970229258,),
    banner="hikari_musicbot_banner",
)


for extension in EXTENSIONS:
    bot.load_extensions(extension)


bot.run()
