from __future__ import annotations

import re
import typing

import lightbulb
from songbird.hikari import Voicebox
from songbird import Source as SongbirdSource
from lyricstranslate import Category

from utils.discord import pass_options
from tools.discord import DefaultEmbed


if typing.TYPE_CHECKING:
    from project_typing import BotContext
    from models.bot import BaseBot


plugin = lightbulb.Plugin("Music")


@plugin.command()
@lightbulb.option("query", "Query for search")
@lightbulb.command(name="search_track", description="Search track")
@lightbulb.implements(lightbulb.SlashCommand)
@pass_options
async def command_search_track(ctx: BotContext, query: str) -> None:
    async with ctx.bot.d.lyrics_translate_client as client:
        suggestions = filter(
            lambda element: element.category == Category.SONGS,
            await client.search(query)
        )

        try:
            suggestion = next(suggestions)
        except StopIteration:
            await ctx.respond(DefaultEmbed(description="`No found`"))
            return

        track_result = await client.get_song_by_url(suggestion.url)
        await ctx.respond(
            DefaultEmbed(description="```" + "\n\n".join(track_result.lyrics) + "```"),
        )


@plugin.command()
@lightbulb.command("join", "Join to channel!")
@lightbulb.implements(lightbulb.SlashCommand)
async def command_join(ctx: BotContext) -> None:
    # TODO: Check is connected

    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_states = states.iterator().filter(lambda i: i.user_id == ctx.author.id)

    try:
        voice_state = await voice_states.__anext__()
    except StopAsyncIteration:
        # FIXME?: Unicode
        # TODO: Check
        await ctx.respond(DefaultEmbed(description="You're not on the music channel(´• ω •)"))
        return

    try:
        await states.iterator().filter(
            lambda i: (
                i.user_id == ctx.bot.me.id  # Check bot id
                and i.channel_id == voice_state.channel_id  # Check channel_id
            )
        ).__anext__()
    except StopAsyncIteration:  # Ok if no found
        pass
    else:
        # Check: Bot already connected
        await ctx.respond(
            DefaultEmbed(
                description="I'm already connected to the music channel(´• ω •)"
            )
        )
        return

    voicebox = await Voicebox.connect(
        client=ctx.bot,
        guild_id=voice_state.guild_id,
        channel_id=voice_state.channel_id,
    )

    await ctx.bot.d.voice_repository.add(ctx.author.id, voicebox)

    await ctx.respond(DefaultEmbed(description="I'm connected(* ^ ω ^)"))


@plugin.command()
@lightbulb.option("query", "Query for play")
@lightbulb.command(name="play", description="Play music!")
@lightbulb.implements(lightbulb.SlashCommand)
@pass_options
async def command_play(ctx: lightbulb.Context, query: str) -> None:

    if re.match(r'^https?://', query) is not None:
        ...

    optional_voicebox = await ctx.bot.d.voice_repository.get(ctx.author.id)
    if optional_voicebox is None:
        await ctx.respond(DefaultEmbed(description="Voicebox is not playing"))
        return
    else:
        voicebox = optional_voicebox

    if not voicebox.is_alive:  # TODO: Check
        await ctx.respond(DefaultEmbed(description="The connection isn't alive"))

    track_handle = await voicebox.play_source(
        await SongbirdSource.ffmpeg("http://dict.youdao.com/dictvoice?audio=nice&type=1"),
    )


def load(bot: BaseBot) -> None:
    bot.add_plugin(plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(plugin)
