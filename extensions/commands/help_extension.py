from __future__ import annotations

import typing

import lightbulb
from lightbulb.ext import filament

if typing.TYPE_CHECKING:
    from project_typing import BotContext
    from bot import BaseBot


plugin = lightbulb.Plugin("Help")


@plugin.command()
@lightbulb.option(
    name="name",
    description="Cog name or command name:D",
    required=False,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="help",
    description="Help command >:3 (Who said nya? Rather, RAWR? It's a Lion!)",
)
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options  # type: ignore
async def command_help(ctx: BotContext, name: str) -> None:
    assert ctx.bot.help_command is not None
    await ctx.bot.help_command.send_help(ctx, name)


def load(bot: BaseBot) -> None:
    bot.add_plugin(plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(plugin)
