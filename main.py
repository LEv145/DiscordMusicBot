import os
from pathlib import Path
from unittest.mock import Mock

from hikari import Intents
from loguru import logger

from config import BOT_TOKEN
from bot import BaseBot
from models.repository import DictVoiceRepository


EXTENSIONS = (
    "extensions.commands.misc_extension",
    "extensions.commands.music_extension",
    "extensions.commands.help_extension",
)

logger.add(Path("log/main.log"), rotation="500 MB")


def main() -> None:
    bot = BaseBot(
        token=BOT_TOKEN,
        database_manager=Mock(),  # FIXME
        owner_ids=(501089151089770517,),
        intents=Intents.GUILD_VOICE_STATES,
        default_enabled_guilds=(867344761970229258,),
        banner="hikari_musicbot_banner",
        voice_voice_repository=DictVoiceRepository(),
    )
    help_command = bot.get_prefix_command("help")
    assert help_command is not None
    bot.remove_command(help_command)

    for extension in EXTENSIONS:
        bot.load_extensions(extension)

    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()


if __name__ == "__main__":
    main()
