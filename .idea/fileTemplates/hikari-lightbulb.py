from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)

import lightbulb


if TYPE_CHECKING:
    from bot import BaseBot


plugin = lightbulb.Plugin("Test")  # TODO: Rename


@plugin.command()
@lightbulb.command(name="ping", description="Ping!")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong<3 ~~")


def load(bot: BaseBot) -> None:
    bot.add_plugin(plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(plugin)
