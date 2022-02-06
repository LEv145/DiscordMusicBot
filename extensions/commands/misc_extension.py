from __future__ import annotations

import typing

import lightbulb

from utils.discord import DefaultEmbed


if typing.TYPE_CHECKING:
    from project_typing import BotContext
    from bot import BaseBot


plugin = lightbulb.Plugin("Misc")


@plugin.command()
@lightbulb.command(name="ping", description="Ping!")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_ping(ctx: BotContext) -> None:
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
