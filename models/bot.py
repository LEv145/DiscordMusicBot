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
        """

        :rtype: object
        """
        super().__init__(token, **kwargs)
        self.d = data_store
        self._user_id: hikari.Snowflake | None = None

        self.subscribe(hikari.StartedEvent, self.on_startup)

    async def on_startup(self, _event: hikari.StartedEvent) -> None:
        me = self.guaranteed_get_me()
        self._user_id = me.id

    @property
    def user_id(self) -> hikari.Snowflake:
        """The application user's ID."""
        if self._user_id is None:
            raise RuntimeError("The bot is not yet initialized, me is unavailable.")

        return self._user_id

    def guaranteed_get_me(self) -> hikari.OwnUser:
        """Guaranteed get me."""
        me = self.get_me()
        if me is None:
            raise RuntimeError("The bot is not yet initialized, me is unavailable.")

        return me
