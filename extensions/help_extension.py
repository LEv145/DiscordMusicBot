from __future__ import annotations

import lightbulb
from models.base_plugin_manager import BasePluginManager
from utils.discord import pass_options


class HelpPluginManager(BasePluginManager):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.load_commands(self)

    @staticmethod
    @lightbulb.option(
        name="name",
        description="Cog name or command name:D",
        required=False,
    )
    @lightbulb.command(
        name="help",
        description="Help command >:3 (Who said nya? Rather, RAWR? It's a Lion!)",
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_options
    async def command_help(ctx: lightbulb.Context, name: str) -> None:
        assert ctx.bot.help_command is not None
        await ctx.bot.help_command.send_help(ctx, name)
