import re

from music_bot.allocation.repositories.models import Track
from music_bot.allocation.repositories import ABCQueueRepository
from modules.lavasnek_player import (
    HikariVoiceLavasnekPlayer,
)
from lavasnek_rs import (
    ConnectionInfo as LavasnekConnectionInfo,
)

from music_source.extractor import TrackExtractor
from music_source.track_models import (
    Track as MusicSourceTrack,
    URLTrack as MusicSourceURLTrack,
)


class BasePlayerManager():
    def __init__(
        self,
        queue_repository: ABCQueueRepository,
        player: HikariVoiceLavasnekPlayer,
        track_extractor: TrackExtractor,
    ) -> None:
        self._queue_repository = queue_repository
        self._player = player
        self._track_extractor = track_extractor

    @property
    def queue_repository(self) -> ABCQueueRepository:
        return self._queue_repository

    async def play(self, guild_id: int, queue_key: int) -> None:
        """Play track.

        Raises:
            TrackNotFoundInQueue
            TrackCannotBeExtractedError
        """
        # queue = await self.get_now_playing(guild_id)
        # if queue is not None:
        #     ...

        queue_track = await self._queue_repository.get_nowait(
            key=queue_key,
        )

        if queue_track is None:
            raise TrackNotFoundInQueueError()

        extractor_result = await self._track_extractor.extract(queue_track.link)

        if not isinstance(extractor_result, MusicSourceTrack):
            raise TrackCannotBeExtractedError()
        track = extractor_result

        node = await self._player.get_guild_node(guild_id)
        node.set_data(dict(current_track=track))  # TODO: Node check

        await self._player.play(
            guild_id=guild_id,
            query=track.stream_url,
        )

    async def join(self, guild_id: int, channel_id: int) -> LavasnekConnectionInfo:
        return await self._player.join(
            guild_id=guild_id,
            channel_id=channel_id,
        )

    async def add_track(self, queue_key: int, query: str) -> None:
        """Add track to queue.

        Raises:
            UnsupportedTrackURL
        """
        if re.match("^https?://.+$", query):
            result = await self._track_extractor.extract(query)

            if isinstance(result, MusicSourceTrack):
                track = result

                await self._queue_repository.put(
                    queue_key,
                    Track(link=track.link, title=track.title),
                )
            elif isinstance(result, list):  # TODO: Better check parsed list[URLTrack]
                tracks: list[MusicSourceURLTrack] = result

                await self._queue_repository.put_many(
                    queue_key,
                    (Track(link=track.link, title=track.title) for track in tracks),
                )
            else:
                raise UnsupportedTrackURLError()
        else:
            raise NotImplemented
            # TODO

    async def get_current_track(self, guild_id: int) -> MusicSourceTrack | None:
        node = await self._player.get_guild_node(guild_id)

        if node is None:
            return None

        return node.get_data()["current_track"]  # TODO

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
    """Base lavasnek_player manager error."""


class TrackNotFoundInQueueError(PlayerManagerError):
    """If track not found in queue."""


class UnsupportedTrackURLError(PlayerManagerError):
    """If track url is unsupported."""


class TrackCannotBeExtractedError(PlayerManagerError):
    """If the track cannot be extracted."""
