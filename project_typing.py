import typing

import hikari
import lightbulb


if typing.TYPE_CHECKING:
    from models.bot import BaseBot


# noinspection PyAbstractClass
class BotContext(lightbulb.Context):
    bot: BaseBot
    guild: hikari.Guild
    guild_id: hikari.Snowflakeish

