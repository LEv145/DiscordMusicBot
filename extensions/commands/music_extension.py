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

from utils.discord import DefaultEmbed


if TYPE_CHECKING:
    from bot import BaseBot


plugin = lightbulb.Plugin("Music")


@lightbulb.option("query", "Text for search")
@plugin.command()
@lightbulb.command(name="search_track", description="Search track")
@lightbulb.implements(lightbulb.SlashCommand)
@filament.utils.pass_options  # type: ignore
async def search_track(ctx: lightbulb.Context, query: str) -> None:
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
            await ctx.respond(DefaultEmbed(description="No found"))
            return

        track_result = await client.get_song_by_url(suggestion.url)
        await ctx.respond(
            DefaultEmbed(description="\n\n".join(track_result.lyrics)),
        )


def load(bot: BaseBot) -> None:
    bot.add_plugin(plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(plugin)
