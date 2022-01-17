from bot import Bot
from disnake.ext import commands


class NoGuildCheck(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


def setup(bot):
    bot.add_cog(NoGuildCheck(bot))
