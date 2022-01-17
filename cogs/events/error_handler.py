import traceback
from disnake import ApplicationCommandInteraction

from termcolor import cprint

from disnake.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot

    @commands.Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
        error = traceback.format_exc()
        cprint(f"{event}: {error}", "yellow", attrs=["bold"])

    @commands.Cog.listener()
    async def on_command_error(
        self,
        _ctx: commands.Context,
        error
    ):
        cprint(
            self._format_command_exception(error),
            color="red",
            attrs=("bold",)
        )

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        _inter: ApplicationCommandInteraction,
        error: commands.CommandError
    ):
        cprint(
            self._format_command_exception(error),
            color="red",
            attrs=("bold",)
        )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        await ctx.message.add_reaction("\N{White Medium Star}")

    def _format_command_exception(self, error: commands.CommandError) -> str:
        error = getattr(error, "original", error)
        return "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
