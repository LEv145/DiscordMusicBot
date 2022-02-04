import os
from pathlib import Path

from hikari import Intents
from loguru import logger

from config import BOT_TOKEN, DATABASE_URL
from database import DatabaseManager
from bot import BaseBot


EXTENSIONS = (
    "extensions.commands.misc_extension",
    "extensions.commands.music_extension",
)

logger.add(Path("log/main.log"), rotation="500 MB")


def main() -> None:
    bot = BaseBot(
        token=BOT_TOKEN,
        database_manager=DatabaseManager(DATABASE_URL),
        owner_ids=(501089151089770517,),
        intents=Intents.NONE,
        default_enabled_guilds=(867344761970229258,),
        banner="hikari_musicbot_banner",
    )

    for extension in EXTENSIONS:
        bot.load_extensions(extension)

    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()


if __name__ == "__main__":
    main()
