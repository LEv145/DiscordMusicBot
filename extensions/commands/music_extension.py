from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)

from injector import Injector
from lyricstranslate import (
    LyricsTranslateClient,
    LyricsTranslateModule,
    Category,
)
import lightbulb
from lightbulb.ext import filament
from songbird.hikari import Voicebox

from utils.discord import DefaultEmbed


if TYPE_CHECKING:
    from bot import BaseBot


plugin = lightbulb.Plugin("Music")


@plugin.command()
@lightbulb.option("query", "Query for search")
@lightbulb.command(name="search_track", description="Search track")
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options  # type: ignore
async def command_search_track(ctx: lightbulb.Context, query: str) -> None:
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
async def command_join(ctx: lightbulb.Context) -> None:
    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_states = states.iterator().filter(lambda i: i.user_id == ctx.author.id)

    try:
        voice_state = await voice_states.__anext__()
    except StopAsyncIteration:
        # FIXME?: Unicode
        await ctx.respond(DefaultEmbed(description="You're not on the music channel(´• ω •)"))
        return

    await Voicebox.connect(
        client=ctx.bot,
        guild_id=ctx.guild_id,
        channel_id=voice_state.channel_id
    )
    await ctx.respond(DefaultEmbed(description="I'm connected(* ^ ω ^)"))


# @plugin.command()
# @lightbulb.option("query", "Query for play")
# @lightbulb.command(name="play", description="Play music!")
# @lightbulb.implements(lightbulb.SlashCommand)
# @filament.utils.pass_options  # type: ignore
# async def command_play(ctx: lightbulb.Context, query: str) -> None:
#     voice = await Voicebox.connect(
#         client=ctx.bot,
#         guild_id=ctx.guild_id,
#         channel_id=ctx.channel_id,
#     )
#     voice.play_source(Source)
#     track_handle = await voice.play_source(Source.ffmpeg())


def load(bot: BaseBot) -> None:
    bot.add_plugin(plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(plugin)
