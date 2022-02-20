from __future__ import annotations

import typing
import re
import logging
from dataclasses import dataclass

import hikari_tools
import lightbulb
import lavasnek_rs
from plugin_manager import PluginManager, pass_plugin
from lyricstranslate import Category
from music_source.track_models import Track

from music_bot.tools.lightbulb_tools import pass_options
from music_bot.utils.general import (
    async_wait_until,
    TimeoutExpired,
)
from music_bot.tools.hikari_tools import DefaultEmbed


if typing.TYPE_CHECKING:
    from src.music_bot.project_typing import BotContext

    from lyricstranslate import LyricsTranslateClient
    from music_source.extractor import TrackExtractor
    from lavasnek_rs import Lavalink as LavalinkClient


_log = logging.getLogger("music_bot.lavalink")


@dataclass
class LavalinkConfig():
    host: str
    password: str


@dataclass
class PluginDataStore(lightbulb.utils.DataStore):
    lavalink_config: LavalinkConfig
    lyrics_translate_client: LyricsTranslateClient
    track_extractor: TrackExtractor


class PluginDataStoreType(PluginDataStore):
    lavalink_client: LavalinkClient  # TODO


class PluginType(lightbulb.Plugin):
    d: PluginDataStoreType


class MusicPluginManager(PluginManager):
    def __init__(
        self,
        name: str,
        data_store: PluginDataStore,
    ) -> None:
        super().__init__(name=name)

        self._plugin._d = data_store

        self._plugin.listener(
            hikari_tools.ShardReadyEvent,
            StaticCommands.start_lavalink,
            bind=True,
        )
        self._plugin.listener(
            hikari_tools.VoiceStateUpdateEvent,
            StaticCommands.on_voice_state_update,
            bind=True,
        )
        self._plugin.listener(
            hikari_tools.VoiceServerUpdateEvent,
            StaticCommands.on_voice_server_update,
            bind=True,
        )

        self.load_commands(StaticCommands)


class StaticCommands():
    @staticmethod
    @lightbulb.add_checks(lightbulb.guild_only)  # TODO guild_only
    @lightbulb.command(
        name="join",
        description="Join to voice channel!",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_plugin
    async def join_command(
        plugin: PluginType,
        ctx: BotContext,
    ) -> None:
        """Joins the voice channel you are in."""
        connection_info = await _join_to_author(ctx, plugin.d.lavalink_client)

        if connection_info is not None:
            await ctx.respond(f"Joined <#{connection_info['channel_id']}>")

    @staticmethod
    @lightbulb.command(
        name="leave",
        description="Leaves the voice channel the bot is in, clearing the queue.",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_plugin
    async def leave_command(
        plugin: PluginType,
        ctx: BotContext,
    ) -> None:
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
            await plugin.d.lavalink_client.destroy(guild_id=ctx.guild_id)
        except lavasnek_rs.NetworkError:
            await ctx.respond("Network error")

        # Leave from channel
        await ctx.bot.update_voice_state(guild=ctx.guild_id, channel=None)
        await plugin.d.lavalink_client.wait_for_connection_info_remove(
            guild_id=ctx.guild_id,
        )

        # Remove the guild node
        await plugin.d.lavalink_client.remove_guild_node(guild_id=ctx.guild_id)

        await ctx.respond("Left voice channel")

    @staticmethod
    @lightbulb.option("query", "Query")
    @lightbulb.command(
        name="play",
        description="Play music",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_options
    @pass_plugin
    async def play_command(
        plugin: PluginType,
        ctx: BotContext,
        query: str,
    ) -> None:  # TODO
        if re.match("^https?://.+$", query):
            result = await plugin.d.track_extractor.extract(query)

            if not isinstance(result, Track):
                return
            stream_url = result.stream_url
        else:
            return

        connection = plugin.d.lavalink_client.get_guild_gateway_connection_info(
            guild_id=ctx.guild_id,
        )

        if connection is None:
            await _join_to_author(ctx, plugin.d.lavalink_client)  # TODO: tests

        tracks_result = await plugin.d.lavalink_client.get_tracks(query=stream_url)

        if not tracks_result.tracks:
            await ctx.respond("No found")
            return

        track = tracks_result.tracks[0]

        try:
            await plugin.d.lavalink_client.play(
                guild_id=ctx.guild_id,
                track=track,
            ).start()
        except lavasnek_rs.NoSessionPresent:
            await ctx.respond("Use join")
            return

        await ctx.respond("Start playing")

    @staticmethod
    @lightbulb.option("query", "Query for search")
    @lightbulb.command(
        name="search_track",
        description="Search track",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_options
    @pass_plugin
    async def search_track_command(
        plugin: PluginType,
        ctx: BotContext,
        query: str,
    ) -> None:
        async with plugin.d.lyrics_translate_client as client:
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

    @staticmethod
    async def start_lavalink(
        plugin: PluginType,
        event: hikari_tools.ShardReadyEvent,
    ) -> None:
        """Event that triggers when the hikari_tools gateway is ready."""
        lavalink_client_builder = (
            # token can be an empty string if you don't want to use lavasnek's lightbulb_tools gateway.
            lavasnek_rs.LavalinkBuilder(bot_id=event.my_user.id, token="")
            .set_host(host=plugin.d.lavalink_config.host)
            .set_password(password=plugin.d.lavalink_config.password)
        )

        lavalink_client_builder.set_start_gateway(False)

        plugin.d.lavalink_client = await lavalink_client_builder.build(EventHandler)

    @staticmethod
    async def on_voice_state_update(
        plugin: PluginType,
        event: hikari_tools.VoiceStateUpdateEvent,
    ) -> None:
        plugin.d.lavalink_client.raw_handle_event_voice_state_update(
            guild_id=event.state.guild_id,
            user_id=event.state.user_id,
            session_id=event.state.session_id,
            channel_id=event.state.channel_id,
        )

    @staticmethod
    async def on_voice_server_update(
        plugin: PluginType,
        event: hikari_tools.VoiceServerUpdateEvent,
    ) -> None:
        assert event.endpoint is not None

        await plugin.d.lavalink_client.raw_handle_event_voice_server_update(
            guild_id=event.guild_id,
            endpoint=event.endpoint,
            token=event.token,
        )


async def _join_to_author(
    ctx: BotContext,
    lavalink_client: LavalinkClient,
) -> lavasnek_rs.ConnectionInfo | None:
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
            function=lavalink_client.wait_for_full_connection_info_insert,
            timeout=3,
            guild_id=ctx.guild_id,
        )
    except (TimeoutError, TimeoutExpired):
        # Bot cannot connect
        await ctx.respond(
            "I was unable to connect to the voice channel, maybe missing permissions¯\\_(ツ)_/¯"
        )
        return None

    await lavalink_client.create_session(connection_info)

    return connection_info


class EventHandler():
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
