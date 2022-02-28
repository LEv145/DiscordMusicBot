import os
import sys
import logging
import toml
from pathlib import Path

import click
import colorlog
import hikari
import lightbulb
from injector import Injector
from lyricstranslate import (
    LyricsTranslateModule,
    LyricsTranslateClient,
)
from music_bot.allocation.repositories import DictQueueRepository

from music_source.clients import (
    YandexMusicClient,
    YandexMusicModule,
)
from music_source.extractor import (
    TrackExtractor,
    YandexMusicTrackExtractor,
    YandexMusicAlbumExtractor,
    YandexMusicPlaylistExtractor,
)

from music_bot.allocation.base_bot import BaseBot
from music_bot.allocation.injector_modules import YandexMusicAPITokenAuthModule
from music_bot.extensions import (
    MiscPluginManager,
    HelpPluginManager,
    MusicPluginManager,
    PluginDataStore,
    LavalinkConfig,
)


######### Logging #########
# TODO
Path("./log").mkdir(parents=True, exist_ok=True)  # Create logs/ if not exist
colorlog.basicConfig(
    level=logging.INFO,
    handlers=(
        logging.StreamHandler(stream=sys.stderr),
        logging.FileHandler(Path("log/main.log")),
    ),
    format=(
        "%(log_color)s%(bold)s%(levelname)-1.1s%(thin)s %(asctime)23.23s %(bold)s%(name)s: "
        "%(thin)s%(message)s%(reset)s"
    ),
)
logging.getLogger("yandex_music").setLevel(logging.FATAL)
_log = colorlog.getLogger("music_bot.main")
######### Logging #########


######### Config #########
with open("config.toml") as fp:
    _config = toml.load(fp)

BOT_TOKEN: str = _config["bot"]["token"]
DATABASE_URL: str = _config["database"]["url"]
YANDEX_MUSIC_TOKEN: str = _config["clients"]["yandex_music"]["token"]
######### Config #########


@click.command()
def main() -> None:
    """Main function."""

    ######### Injectors #########
    lyrics_translate_injector = Injector(LyricsTranslateModule())
    yandex_music_injector = Injector(
        modules=(
            YandexMusicModule(),
            YandexMusicAPITokenAuthModule(YANDEX_MUSIC_TOKEN),
        ),
    )
    ######### Injectors #########

    bot = BaseBot(
        token=BOT_TOKEN,
        owner_ids=[501089151089770517],
        intents=hikari.Intents.GUILD_VOICE_STATES,
        default_enabled_guilds=[867344761970229258],
        banner="hikari_musicbot_banner",
        logs=None,
        help_class=None,
    )
    # Add help command
    bot.help_command = lightbulb.DefaultHelpCommand(bot)

    bot.add_plugin(MiscPluginManager("Misc").get_plugin())
    bot.add_plugin(HelpPluginManager("Help").get_plugin())
    bot.add_plugin(
        MusicPluginManager(
            "Music",
            data_store=PluginDataStore(
                lavalink_config=LavalinkConfig(
                    host="127.0.0.1",
                    password="TheCat",
                    track_extractor=TrackExtractor([
                        YandexMusicPlaylistExtractor(yandex_music_injector.get(YandexMusicClient)),
                        YandexMusicAlbumExtractor(yandex_music_injector.get(YandexMusicClient)),
                        YandexMusicTrackExtractor(yandex_music_injector.get(YandexMusicClient)),
                    ]),
                    queue_repository=DictQueueRepository(),
                ),
                lyrics_translate_client=lyrics_translate_injector.get(LyricsTranslateClient),
            )
        ).get_plugin()
    )

    # Start bot
    if os.name != "nt":
        import uvloop
        uvloop.install()
        _log.info("Uvloop enabled")

    bot.run()


if __name__ == "__main__":
    main()
