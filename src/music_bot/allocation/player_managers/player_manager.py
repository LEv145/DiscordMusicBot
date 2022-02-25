from allocation.abс_repositories import ABCQueueRepository

from music_bot.allocation.tools.lavasnek.lavasnek_player import HikariVoiceLavasnekPlayer


class BasePlayerManager():
    def __init__(
        self,
        queue_repository: ABCQueueRepository,
        player: HikariVoiceLavasnekPlayer,
    ) -> None:
        self._queue_repository = queue_repository
        self._player = player

    @property
    def queue_repository(self) -> ABCQueueRepository:
        return self._queue_repository

    async def play(self, guild_id: int, queue_key: int) -> None:
        track = await self._queue_repository.get_nowait(
            key=queue_key,
        )

        if track is None:
            raise TrackNotFoundInQueue()

        await self._player.play(
            guild_id=guild_id,
            track=track,
        )

    def raw_handle_event_voice_state_update(
        self,
        guild_id: int,
        user_id: int,
        session_id: str,
        channel_id: int | None,
    ) -> None:
        self._player.raw_handle_event_voice_state_update(
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
        await self._player.raw_handle_event_voice_server_update(
            guild_id=guild_id,
            endpoint=endpoint,
            token=token,
        )


class PlayerManagerError(Exception):
    """Base player manager error."""


class TrackNotFoundInQueue(PlayerManagerError):
    """If track not found in queue."""
