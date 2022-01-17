import traceback

from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from loguru import logger


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot

    @commands.Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
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
    ):
        logger.error(error)

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        _inter: ApplicationCommandInteraction,
        error: commands.CommandError
    ):
        logger.error(error)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        await ctx.message.add_reaction("\N{White Medium Star}")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
