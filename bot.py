from __future__ import annotations

import typing

from lightbulb import BotApp


if typing.TYPE_CHECKING:
    from database import DatabaseManager


# noinspection PyAbstractClass
class BaseBot(BotApp):
    def __init__(
        self,
        token: str,
        database_manager: DatabaseManager,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(token, **kwargs)
        self.d.database = database_manager
