from __future__ import annotations

import typing
import logging
from dataclasses import dataclass

import hikari
import lavasnek_rs
import lightbulb
from lightbulb_plugin_manager import PluginManager, pass_plugin
from allocation.repositories import ABCQueueRepository

from music_bot.allocation.player_managers import (
    BasePlayerManager,
    TrackNotFoundInQueue,
)
from music_bot.allocation.tools.lavasnek import HikariVoiceLavasnekPlayer
from music_bot.allocation.tools.lightbulb import pass_options
from music_bot.utils.asyncio import (
    async_wait_until,
    TimeoutExpired,
)
from music_bot.allocation.tools.hikari import DefaultEmbed


if typing.TYPE_CHECKING:
    from music_bot.allocation.tools.lightbulb import BotContextType, BaseBot

    from lyricstranslate import LyricsTranslateClient
    from music_source.extractor import TrackExtractor
    from lavasnek_rs import Lavalink as LavalinkClient


_log = logging.getLogger(__name__)


@dataclass
class LavalinkConfig():
    password: str
    host: str
    track_extractor: TrackExtractor
    queue_repository: ABCQueueRepository


# noinspection PyAttributeOutsideInit
class PluginDataStore(lightbulb.utils.DataStore):
    def __init__(
        self,
        lavalink_config: LavalinkConfig,
        lyrics_translate_client: LyricsTranslateClient,
    ) -> None:
        self.lavalink_config = lavalink_config
        self.lyrics_translate_client = lyrics_translate_client

        self._lavasnek_player_manager: BasePlayerManager | None = None

    def get_lavasnek_player_manager(self) -> BasePlayerManager:
        if self._lavasnek_player_manager is None:
            raise RuntimeError("Lavasnek player is not registered")

        return self._lavasnek_player_manager

    def set_lavasnek_player_manager(self, value: BasePlayerManager) -> None:
        self._lavasnek_player_manager = value


class PluginType(lightbulb.Plugin):
    d: PluginDataStore


class MusicPluginManager(PluginManager):
    def __init__(
        self,
        name: str,
        data_store: PluginDataStore,
    ) -> None:
        super().__init__(name=name)
        self._plugin._d = data_store

        self._plugin.listener(
            hikari.ShardReadyEvent,
            self.start_lavalink,
            bind=True,
        )
        self._plugin.listener(
            hikari.VoiceStateUpdateEvent,
            self.on_voice_state_update,
            bind=True,
        )
        self._plugin.listener(
            hikari.VoiceServerUpdateEvent,
            self.on_voice_server_update,
            bind=True,
        )

        self.load_commands(StaticCommands)

    @staticmethod
    async def start_lavalink(
        plugin: PluginType,
        event: hikari.ShardReadyEvent,
    ) -> None:
        """Event that triggers when the hikari gateway is ready."""
        bot: BaseBot = event.app  # type: ignore

        lavalink_client_builder = (
            # token can be an empty string if you don't want to use lavasnek's lightbulb gateway.
            lavasnek_rs.LavalinkBuilder(bot_id=event.my_user.id, token="")
            .set_host(host=plugin.d.lavalink_config.host)
            .set_password(password=plugin.d.lavalink_config.password)
        )

        lavalink_client_builder.set_start_gateway(False)

        lavalink_client = await lavalink_client_builder.build(EventHandler)

        plugin.d.set_lavasnek_player_manager(
            BasePlayerManager(
                queue_repository=plugin.d.lavalink_config.queue_repository,
                player=HikariVoiceLavasnekPlayer(
                    lavasnek_client=lavalink_client,
                    bot=bot,
                )
            )
        )

    @staticmethod
    async def on_voice_state_update(
        plugin: PluginType,
        event: hikari.VoiceStateUpdateEvent,
    ) -> None:

        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

        lavasnek_player_manager.raw_handle_event_voice_state_update(
            guild_id=event.state.guild_id,
            user_id=event.state.user_id,
            session_id=event.state.session_id,
            channel_id=event.state.channel_id,
        )

    @staticmethod
    async def on_voice_server_update(
        plugin: PluginType,
        event: hikari.VoiceServerUpdateEvent,
    ) -> None:
        assert event.endpoint is not None

        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

        await lavasnek_player_manager.raw_handle_event_voice_server_update(
            guild_id=event.guild_id,
            endpoint=event.endpoint,
            token=event.token,
        )


class StaticCommands():
    @staticmethod
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
        ctx: BotContextType,
    ) -> None:
        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

        try:
            await lavasnek_player_manager.play(
                guild_id=ctx.guild_id,
                queue_key=ctx.guild_id,
            )
        except TrackNotFoundInQueue:
            await ctx.respond(
                DefaultEmbed(
                    title="The queue is empty, add something",
                )
            )


async def _join_to_author(
    ctx: BotContextType,
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
