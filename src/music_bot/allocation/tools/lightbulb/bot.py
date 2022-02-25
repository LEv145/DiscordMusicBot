# TODO?: Move to models

from __future__ import annotations

import typing

import hikari
import lightbulb


# noinspection PyAbstractClass
class BaseBot(lightbulb.BotApp):
    """My bot:3."""

    def __init__(
        self,
        token: str,
        **kwargs: typing.Any,
    ) -> None:
        """Base bot class."""
        super().__init__(token, **kwargs)
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


# noinspection PyAbstractClass
class BotContextType(lightbulb.Context):
    bot: BaseBot
    guild: hikari.Guild
    guild_id: hikari.Snowflakeish
