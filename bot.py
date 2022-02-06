from __future__ import annotations

import typing

import lightbulb


if typing.TYPE_CHECKING:
    from models.abc_repository import ABCVoiceRepository
    from database import DatabaseManager

    from lyricstranslate import LyricsTranslateClient


class BotDataStore(lightbulb.utils.DataStore):
    def __init__(
        self,
        database: DatabaseManager,
        voice_repository: ABCVoiceRepository,
        lyrics_translate_client: LyricsTranslateClient,
    ):
        self.database = database
        self.voice_repository = voice_repository
        self.lyrics_translate_client = lyrics_translate_client


# noinspection PyAbstractClass
class BaseBot(lightbulb.BotApp):
    """My bot:3."""
    d: BotDataStore

    def __init__(
        self,
        token: str,
        data_store: BotDataStore,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(token, **kwargs)
        self.d = data_store

