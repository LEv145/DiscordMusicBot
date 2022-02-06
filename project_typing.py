import typing

import hikari
import lightbulb


if typing.TYPE_CHECKING:
    from bot import BaseBot


class BotContext(lightbulb.Context):
    bot: BaseBot
    guild: hikari.Guild
    guild_id: hikari.Snowflakeish

