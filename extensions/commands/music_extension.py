from __future__ import annotations

import re
import typing

from injector import Injector
from lyricstranslate import (
    LyricsTranslateClient,
    LyricsTranslateModule,
    Category,
)
import lightbulb
from lightbulb.ext import filament
from songbird.hikari import Voicebox
from songbird import Source as SongbirdSource

from utils.discord import DefaultEmbed


if typing.TYPE_CHECKING:
    from project_typing import BotContext
    from bot import BaseBot


plugin = lightbulb.Plugin("Music")


@plugin.command()
@lightbulb.option("query", "Query for search")
@lightbulb.command(name="search_track", description="Search track")
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options  # type: ignore
async def command_search_track(ctx: BotContext, query: str) -> None:
    injector = Injector(LyricsTranslateModule)
    client_ = injector.get(LyricsTranslateClient)

    async with client_ as client:
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
@filament.utils.pass_options  # type: ignore
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
