from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)

import lightbulb

from utils.discord import DefaultEmbed


if TYPE_CHECKING:
    from bot import BaseBot


plugin = lightbulb.Plugin("Misc")


@plugin.command()
@lightbulb.command(name="ping", description="Ping!")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(
        DefaultEmbed(
            title="\N{Table Tennis Paddle and Ball} Pong!",
            description=f"Latency: `{round(ctx.app.heartbeat_latency * 1000, 2)}ms`",
        )
    )


def load(bot: BaseBot) -> None:
    bot.add_plugin(plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(plugin)
