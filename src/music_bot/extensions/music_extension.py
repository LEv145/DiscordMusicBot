from __future__ import annotations

import typing
import logging
from dataclasses import dataclass

import hikari
import lavasnek_rs
import lightbulb
from modules.lavasnek_player import HikariVoiceLavasnekPlayer
from music_bot.allocation.repositories import ABCQueueRepository
from lightbulb_plugin_manager import PluginManager, pass_plugin

from music_bot.allocation.player_managers import (
    BasePlayerManager,
    TrackNotFoundInQueueError,
    UnsupportedTrackURLError,
)
from music_bot.allocation.music_source_embed_builder import MusicSourceEmbedBuilder
from music_bot.tools import pass_options
from music_bot.allocation.default_embed import DefaultEmbed



if typing.TYPE_CHECKING:
    from music_bot.tools import BotContextType, BaseBot

    from lyricstranslate import LyricsTranslateClient
    from music_source.extractor import TrackExtractor


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
        super().__init__()

        self.lavalink_config = lavalink_config
        self.lyrics_translate_client = lyrics_translate_client

        self._lavasnek_player_manager: BasePlayerManager | None = None

    def get_lavasnek_player_manager(self) -> BasePlayerManager:
        if self._lavasnek_player_manager is None:
            raise RuntimeError("Lavasnek lavasnek_player is not registered")

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
        """Event that triggers when the default_embed gateway is ready."""
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
                ),
                track_extractor=plugin.d.lavalink_config.track_extractor,
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
    @pass_plugin
    async def play_command(
        plugin: PluginType,
        ctx: BotContextType,
    ) -> None:
        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

        try:
            await lavasnek_player_manager.play(
                queue_key=ctx.guild_id,
                guild_id=ctx.guild_id,
            )
        except TrackNotFoundInQueueError:
            await ctx.respond(
                DefaultEmbed(
                    title="The queue is empty, add something",
                ),
            )
        else:
            await ctx.respond(DefaultEmbed(title="Starting playing..."))

    @staticmethod
    @lightbulb.option(
        "query",
        "Query of track",
    )
    @lightbulb.command(
        name="add",
        description="Add track to queue",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_options
    @pass_plugin
    async def add_command(
        plugin: PluginType,
        ctx: BotContextType,
        query: str,
    ) -> None:
        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

        try:
            await lavasnek_player_manager.add_track(
                queue_key=ctx.guild_id,
                query=query,
            )
        except UnsupportedTrackURLError:
            await ctx.respond(
                DefaultEmbed(
                    title="Track url is not supported",
                ),
            )
        else:
            await ctx.respond(
                DefaultEmbed(
                    title="Track url successfully added!",
                ),
            )

    @staticmethod
    @lightbulb.command(
        name="current_track",
        description="What's the current track?",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_plugin
    async def current_track_command(
        plugin: PluginType,
        ctx: BotContextType,
    ) -> None:
        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

        current_track = await lavasnek_player_manager.get_current_track(
            guild_id=ctx.guild_id,
        )

        embed_builder = MusicSourceEmbedBuilder(current_track)
        await ctx.respond(embed=embed_builder.get_embed())


    @staticmethod
    @lightbulb.command(
        name="join",
        description="Join to music channel!",
        auto_defer=True,
    )
    @lightbulb.implements(lightbulb.SlashCommand)
    @pass_plugin
    async def join_command(
        plugin: PluginType,
        ctx: BotContextType,
    ) -> None:
        lavasnek_player_manager = plugin.d.get_lavasnek_player_manager()

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
            ...  # TODO
        else:
            await ctx.respond(DefaultEmbed(description="I'm already connected!!1!OwO"))
            return None

        try:
            connection_info = await lavasnek_player_manager.join(
                guild_id=ctx.guild_id,
                channel_id=author_voice_state.channel_id,
            )
        except Exception:
            ...  # TODO

        await ctx.respond(f"Joined <#{connection_info['channel_id']}>")


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
