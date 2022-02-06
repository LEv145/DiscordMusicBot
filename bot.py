from __future__ import annotations

import typing

import hikari
import lightbulb


if typing.TYPE_CHECKING:
    from models.abc_repository import ABCVoiceRepository
    from database import DatabaseManager

    from lyricstranslate import LyricsTranslateClient


class BotDataStore(lightbulb.utils.DataStore):
    def __init__(
        self,
        database_manager: DatabaseManager,
        voice_repository: ABCVoiceRepository,
        lyrics_translate_client: LyricsTranslateClient,
    ):
        super().__init__()
        self.database_manager = database_manager
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
        self._me: hikari.OwnUser | None = None

        self.subscribe(hikari.StartedEvent, self.on_startup)

    async def on_startup(self, _event: hikari.StartedEvent) -> None:
        self._me = self.get_me()

    @property
    def me(self) -> hikari.OwnUser:
        """The application user's ID."""
        if self._me is None:
            raise RuntimeError("The bot is not yet initialized, me is unavailable.")

        return self._me

    def get_me(self) -> hikari.OwnUser | None:
        result = super().get_me()
        self._me = result

        return result
