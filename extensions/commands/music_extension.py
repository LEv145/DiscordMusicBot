from __future__ import annotations

import asyncio
import typing
import re
import logging

import hikari
import lightbulb
import lavasnek_rs
from lyricstranslate import Category

from utils.discord import pass_options
from utils.general import (
    async_wait_until,
    TimeoutExpired,
)
from tools.discord import DefaultEmbed
from project_typing import BotContext
from models.bot import BaseBot
from models.bot import BotDataStore


_log = logging.getLogger("music_bot.lavalink")


################## Typing ##################
class ExtensionBotDataStore(BotDataStore):
    lavalink_client: lavasnek_rs.Lavalink


# noinspection PyAbstractClass
class ExtensionBot(BaseBot):
    d: ExtensionBotDataStore


# noinspection PyAbstractClass
class ExtensionContext(BotContext):
    bot: ExtensionBot
################## Typing ##################


class EventHandler:
    """Events from the Lavalink server"""
    async def track_start(
        self,
        _lavalink_client: lavasnek_rs.Lavalink,
        event: lavasnek_rs.TrackStart,
    ) -> None:
        _log.info(f"Track started on guild: {event.guild_id}")

    async def track_finish(
        self,
        _lavalink_client: lavasnek_rs.Lavalink,
        event: lavasnek_rs.TrackFinish,
    ) -> None:
        _log.info(f"Track finished on guild: {event.guild_id}")

    async def track_exception(
        self,
        _lavalink_client: lavasnek_rs.Lavalink,
        event: lavasnek_rs.TrackException,
    ) -> None:
        _log.warning(f"Track exception event happened on guild: {event.guild_id}")


_plugin = lightbulb.Plugin("Music")


@_plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)  # TODO guild_only
@lightbulb.command(
    name="join",
    description="Join to voice channel!",
    auto_defer=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _join_command(ctx: ExtensionContext) -> None:
    """Joins the voice channel you are in."""
    connection_info = await _join_to_author(ctx)

    if connection_info is not None:
        await ctx.respond(f"Joined <#{connection_info['channel_id']}>")


@_plugin.command()
@lightbulb.command(
    name="leave",
    description="Leaves the voice channel the bot is in, clearing the queue.",
    auto_defer=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _leave_command(ctx: ExtensionContext) -> None:
    """Leaves the voice channel the bot is in, clearing the queue."""
    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)

    # Check if bot in voice channel
    try:
        await states.iterator().filter(
            lambda i: i.user_id == ctx.bot.user_id
        ).__anext__()
    except StopAsyncIteration:
        await ctx.respond("Not in a voice channel")
        return None

    # Stops the session in Lavalink of the guild
    try:
        await ctx.bot.d.lavalink_client.destroy(guild_id=ctx.guild_id)
    except lavasnek_rs.NetworkError:
        await ctx.respond("Network error")

    # Leave from channel
    await ctx.bot.update_voice_state(guild=ctx.guild_id, channel=None)
    await ctx.bot.d.lavalink_client.wait_for_connection_info_remove(
        guild_id=ctx.guild_id,
    )

    # Remove the guild node
    await ctx.bot.d.lavalink_client.remove_guild_node(guild_id=ctx.guild_id)

    await ctx.respond("Left voice channel")


@_plugin.command()
@lightbulb.option("query", "Query")
@lightbulb.command(
    name="play",
    description="Play music",
    auto_defer=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
@pass_options
async def _play_command(ctx: ExtensionContext, query: str) -> None:  # TODO
    # if re.match("^https?://.+$", query):
    #     ...
    # else:
    #     ...

    connection = ctx.bot.d.lavalink_client.get_guild_gateway_connection_info(
        guild_id=ctx.guild_id,
    )

    if connection is None:
        await _join_to_author(ctx)

    tracks_result = await ctx.bot.d.lavalink_client.get_tracks(
        query="http://dict.youdao.com/dictvoice?audio=nice&type=1",
    )
    track = tracks_result.tracks[0]

    try:
        await ctx.bot.d.lavalink_client.play(
            guild_id=ctx.guild_id,
            track=track,
        ).start()
    except lavasnek_rs.NoSessionPresent:
        await ctx.respond("Use join")
        return

    await ctx.respond("Start playing")


@_plugin.command()
@lightbulb.option("query", "Query for search")
@lightbulb.command(
    name="search_track",
    description="Search track",
    auto_defer=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
@pass_options
async def _search_track_command(ctx: BotContext, query: str) -> None:
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


@_plugin.listener(hikari.ShardReadyEvent)
async def _start_lavalink(event: hikari.ShardReadyEvent) -> None:
    """Event that triggers when the hikari gateway is ready."""
    bot: ExtensionBot = event.app  # type: ignore

    lavalink_client_builder = (
        # token can be an empty string if you don't want to use lavasnek's discord gateway.
        lavasnek_rs.LavalinkBuilder(bot_id=event.my_user.id, token="")
        .set_host(host="127.0.0.1")
        .set_password(password="TheCat")  # Do not change, pls
    )

    lavalink_client_builder.set_start_gateway(False)

    bot.d.lavalink_client = await lavalink_client_builder.build(EventHandler)


@_plugin.listener(hikari.VoiceStateUpdateEvent)
async def _on_voice_state_update(event: hikari.VoiceStateUpdateEvent) -> None:
    bot: ExtensionBot = event.app  # type: ignore

    bot.d.lavalink_client.raw_handle_event_voice_state_update(
        guild_id=event.state.guild_id,
        user_id=event.state.user_id,
        session_id=event.state.session_id,
        channel_id=event.state.channel_id,
    )


@_plugin.listener(hikari.VoiceServerUpdateEvent)
async def _on_voice_server_update(event: hikari.VoiceServerUpdateEvent) -> None:
    assert event.endpoint is not None

    bot: ExtensionBot = event.app  # type: ignore

    await bot.d.lavalink_client.raw_handle_event_voice_server_update(
        guild_id=event.guild_id,
        endpoint=event.endpoint,
        token=event.token,
    )


async def _join_to_author(ctx: ExtensionContext) -> lavasnek_rs.ConnectionInfo | None:
    """Join the bot to the voice channel where the member is located."""
    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)

    # Check if author in voice channel
    try:
        author_voice_state = await states.iterator().filter(
            lambda i: i.user_id == ctx.author.id
        ).__anext__()
    except StopAsyncIteration:
        await ctx.respond(DefaultEmbed(description="You're not on the music channel(´• ω •)"))
        return None

    # Check if bot is already connected to user channel
    try:
        await states.iterator().filter(
            lambda i: (
                i.user_id == ctx.bot.user_id and
                i.channel_id == author_voice_state.channel_id
            )
        ).__anext__()
    except StopAsyncIteration:
        ...
    else:
        await ctx.respond(DefaultEmbed(description="I'm already connected!!1!OwO"))
        return None

    # Connect to channel
    await ctx.bot.update_voice_state(
        guild=ctx.guild_id,
        channel=author_voice_state.channel_id,
        self_deaf=True,
    )

    try:
        connection_info: lavasnek_rs.ConnectionInfo = await async_wait_until(
            condition=lambda i: i["channel_id"] == author_voice_state.channel_id,
            function=ctx.bot.d.lavalink_client.wait_for_full_connection_info_insert,
            timeout=3,
            guild_id=ctx.guild_id,
        )
    except (TimeoutError, TimeoutExpired):
        # Bot cannot connect
        await ctx.respond(
            "I was unable to connect to the voice channel, maybe missing permissions¯\\_(ツ)_/¯"
        )
        return None

    await ctx.bot.d.lavalink_client.create_session(connection_info)

    return connection_info


# @plugin.command()
# @lightbulb.command("join", "Join to channel!")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def command_join(ctx: BotContext) -> None:
#     # TODO: Check is connected
#
#    states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
#    voice_states = states.iterator().filter(lambda i: i.user_id == ctx.author.id)
#
#    try:
#        voice_state = await voice_states.__anext__()
#    except StopAsyncIteration:
#        # FIXME?: Unicode
#        # TODO: Check
#        await ctx.respond(DefaultEmbed(description="You're not on the music channel(´• ω •)"))
#        return
#
#     try:
#         await states.iterator().filter(
#             lambda i: (
#                 i.user_id == ctx.bot.me.id  # Check bot id
#                 and i.channel_id == voice_state.channel_id  # Check channel_id
#             )
#         ).__anext__()
#     except StopAsyncIteration:  # Ok if no found
#         pass
#     else:
#         # Check: Bot already connected
#         await ctx.respond(
#             DefaultEmbed(
#                 description="I'm already connected to the music channel(´• ω •)"
#             )
#         )
#         return
#
#     voicebox = await Voicebox.connect(
#         client=ctx.bot,
#         guild_id=voice_state.guild_id,
#         channel_id=voice_state.channel_id,
#     )
#
#     await ctx.bot.d.voice_repository.add(ctx.author.id, voicebox)
#
#     await ctx.respond(DefaultEmbed(description="I'm connected(* ^ ω ^)"))
#
#
# @plugin.command()
# @lightbulb.option("query", "Query for play")
# @lightbulb.command(name="play", description="Play music!")
# @lightbulb.implements(lightbulb.SlashCommand)
# @pass_options
# async def command_play(ctx: lightbulb.Context, query: str) -> None:
#
#     if re.match(r'^https?://', query) is not None:
#         ...
#
#     optional_voicebox = await ctx.bot.d.voice_repository.get(ctx.author.id)
#     if optional_voicebox is None:
#         await ctx.respond(DefaultEmbed(description="Voicebox is not playing"))
#         return
#     else:
#         voicebox = optional_voicebox
#
#     if not voicebox.is_alive:  # TODO: Check
#         await ctx.respond(DefaultEmbed(description="The connection isn't alive"))
#
#     track_handle = await voicebox.play_source(
#         await SongbirdSource.ffmpeg("http://dict.youdao.com/dictvoice?audio=nice&type=1"),
#     )


def load(bot: BaseBot) -> None:
    bot.add_plugin(_plugin)


def unload(bot: BaseBot) -> None:
    bot.remove_plugin(_plugin)
