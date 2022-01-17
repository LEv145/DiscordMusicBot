from typing import (
    TYPE_CHECKING,
)
from disnake.ext import commands


if TYPE_CHECKING:
    from bot import Bot


class NoGuildCheck(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


def setup(bot):
    bot.add_cog(NoGuildCheck(bot))
