from hikari import GatewayBot
from lavasnek_rs import (
    Lavalink,
    ConnectionInfo,
    Node,
)

from .utils.asyncio import async_wait_until


class HikariVoiceLavasnekPlayer():
    def __init__(
        self,
        lavasnek_client: Lavalink,
        bot: GatewayBot,
    ):
        self._bot = bot
        self._lavasnek_client = lavasnek_client

    async def join(
        self,
        guild_id: int,
        channel_id: int,
        timeout: int = 3,
    ) -> ConnectionInfo:
        """Join to music channel.

        Raises:
            utils.general.TimeoutExpired: If waiting time did not pass by timeout.
        """

        await self._connect_to_channel(guild_id=guild_id, channel_id=channel_id)

        connection_info = await self._get_channel_connection_info(
            guild_id=guild_id,
            channel_id=channel_id,
            timeout=timeout,
        )

        await self._lavasnek_client.create_session(connection_info)
        return connection_info

    async def stop(self, guild_id: int) -> None:
        """Stop playing track.

        Raises:
            lavasnek_rs.NetworkError: If lavalink network error.
        """

        await self._lavasnek_client.stop(guild_id)

    async def pause(self, guild_id: int) -> None:
        """Pause guild voice."""

        await self._lavasnek_client.pause(guild_id)

    async def unpause(self, guild_id: int) -> None:
        """Unpause guild voice."""

        await self._lavasnek_client.resume(guild_id)

    async def paused(self, guild_id: int) -> bool:
        """Check paused status."""

        node = await self._lavasnek_client.get_guild_node(guild_id)

        if node is None:
            raise ValueError("Guild node no found")

        return node.is_paused

    async def leave(self, guild_id: int) -> None:
        """Leave bot from guild voice.

        Raises:
            RuntimeError: If guild passed isn't covered
                by any of the shards in this sharded client.
        """

        await self._bot.update_voice_state(guild_id, None)
        await self._lavasnek_client.wait_for_connection_info_remove(guild_id)

    async def play(self, guild_id: int, query: str) -> None:
        """Play track.

        Raises:
            TracksNoFound: If track no found.
            lavasnek_rs.NetworkError: If lavalink network error.
        """
        tracks_result = await self._lavasnek_client.get_tracks(query)
        tracks = tracks_result.tracks

        if not tracks:
            raise TracksNoFound()

        track = tracks[0]

        await self._lavasnek_client.play(guild_id=guild_id, track=track).queue()

    async def get_guild_node(self, guild_id: int) -> Node | None:
        return await self._lavasnek_client.get_guild_node(guild_id)

    def raw_handle_event_voice_state_update(
        self,
        guild_id: int,
        user_id: int,
        session_id: str,
        channel_id: int | None,
    ) -> None:
        self._lavasnek_client.raw_handle_event_voice_state_update(
            guild_id=guild_id,
            user_id=user_id,
            session_id=session_id,
            channel_id=channel_id,
        )

    async def raw_handle_event_voice_server_update(
        self,
        guild_id: int,
        endpoint: str,
        token: str,
    ) -> None:
        await self._lavasnek_client.raw_handle_event_voice_server_update(
            guild_id=guild_id,
            endpoint=endpoint,
            token=token,
        )

    async def _connect_to_channel(
        self,
        guild_id: int,
        channel_id: int,
    ) -> None:
        """Connect to music channel.

        Raises:
            RuntimeError: If guild passed isn't covered
                by any of the shards in this sharded client.
        """

        await self._bot.update_voice_state(
            guild_id,
            channel_id,
            self_deaf=True,
        )

    async def _get_channel_connection_info(
        self,
        guild_id: int,
        channel_id: int,
        timeout: int = 3,
    ) -> ConnectionInfo:
        """Get connection info of channel.

        Raises:
            utils.general.TimeoutExpired: If waiting time did not pass by timeout.
        """

        connection_info: ConnectionInfo = await async_wait_until(
            condition=lambda i: i["channel_id"] == channel_id,
            function=self._lavasnek_client.wait_for_full_connection_info_insert,
            timeout=timeout,
            guild_id=guild_id,
        )
        return connection_info


class HikariVoiceLavasnekPlayerError(Exception):
    """Base default_embed voice lavasnek lavasnek_player error."""


class TracksNoFound(HikariVoiceLavasnekPlayerError):
    """Lavalink couldn't get the track."""
