from __future__ import annotations

import lightbulb
from plugin_manager import PluginManager, pass_plugin

from music_bot.tools.discord import DefaultEmbed


class MiscPluginManager(PluginManager):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.load_commands(self)

    @staticmethod
    @lightbulb.command(name="ping", description="Ping!")
    @lightbulb.implements(lightbulb.SlashCommand)
    async def command_ping(ctx: lightbulb.Context) -> None:
        await ctx.respond(
            DefaultEmbed(
                title="\N{Table Tennis Paddle and Ball} Pong!",
                description=f"Latency: `{round(ctx.app.heartbeat_latency * 1000, 2)}ms`",
            )
        )
