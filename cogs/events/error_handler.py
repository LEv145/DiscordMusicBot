from typing import (
    Any,
    TYPE_CHECKING,
)

from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from loguru import logger

if TYPE_CHECKING:
    from bot import Bot


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(
        self,
        event: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        logger.exception(
            f"Event: {event}\n"
            f"Args: {args}\n"
            f"Kwargs: {kwargs}"
        )

    @commands.Cog.listener()
    async def on_command_error(
        self,
        _ctx: commands.Context,
        error: commands.CommandError,
    ) -> None:
        logger.error(error)

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        _inter: ApplicationCommandInteraction,
        error: commands.CommandError,
    ) -> None:
        logger.error(error)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context) -> None:
        await ctx.message.add_reaction("\N{White Medium Star}")


def setup(bot: Bot) -> None:
    bot.add_cog(ErrorHandler(bot))
