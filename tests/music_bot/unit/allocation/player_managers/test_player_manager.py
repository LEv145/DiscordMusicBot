import unittest
from unittest.mock import AsyncMock, MagicMock

from music_bot.allocation.player_managers import (
    BasePlayerManager,
    TrackNotFoundInQueueError,
)


class TestBasePlayerManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._queue_repository_mock = AsyncMock()
        self._player_mock = AsyncMock()
        self._track_extractor = AsyncMock()

        self._player_manager = BasePlayerManager(
            queue_repository=self._queue_repository_mock,
            player=self._player_mock,
            track_extractor=self._track_extractor,
        )

    async def test_play(self) -> None:
        mock_track = MagicMock()
        self._queue_repository_mock.get_nowait = AsyncMock(
            return_value=mock_track,
        )

        await self._player_manager.play(
            guild_id=867344761970229258,
            queue_key=501089151089770517,
        )

        self._queue_repository_mock.get_nowait.assert_awaited_once_with(
            key=501089151089770517,
        )
        self._player_mock.play.assert_awaited_once_with(
            guild_id=867344761970229258,
            track=mock_track,
        )


        # Test if track no found
        self._queue_repository_mock.get_nowait = AsyncMock(
            return_value=None,
        )
        with self.assertRaises(TrackNotFoundInQueueError):
            await self._player_manager.play(
                guild_id=867344761970229258,
                queue_key=501089151089770517,
            )
