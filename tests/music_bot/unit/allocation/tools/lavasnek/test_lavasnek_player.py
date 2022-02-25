import unittest
from unittest.mock import AsyncMock, MagicMock

from music_bot.allocation.tools.lavasnek.lavasnek_player import (
    HikariVoiceLavasnekPlayer,
    GatewayBot,
    TracksNoFound,
)


class TestHikariVoiceLavasnekPlayer(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.mock_lavasnek_client = AsyncMock()
        self.mock_bot = AsyncMock(GatewayBot)

        self.player = HikariVoiceLavasnekPlayer(
            lavasnek_client=self.mock_lavasnek_client,
            bot=self.mock_bot,
        )


    async def test_connect_to_channel(self) -> None:
        await self.player.connect_to_channel(
            guild_id=867344761970229258,
            channel_id=941028651057709057,
        )
        self.mock_bot.update_voice_state.assert_called_once_with(
            867344761970229258,
            941028651057709057,
            self_deaf=True,
        )

    async def test_get_connection_info(self) -> None:
        connection_info_mock = MagicMock()
        connection_info_mock.__getitem__.return_value = 941028651057709057

        self.mock_lavasnek_client.wait_for_full_connection_info_insert = (
            AsyncMock(return_value=connection_info_mock)
        )
        result = await self.player.get_channel_connection_info(
            guild_id=867344761970229258,
            channel_id=941028651057709057,
            timeout=0,
        )
        self.assertIs(result, connection_info_mock)

    async def test_join(self) -> None:
        self.player.connect_to_channel = AsyncMock()
        self.player.get_channel_connection_info = AsyncMock()

        await self.player.join(
            guild_id=867344761970229258,
            channel_id=941028651057709057,
            timeout=2,
        )

        self.player.connect_to_channel.assert_called_once_with(
            guild_id=867344761970229258,
            channel_id=941028651057709057,
        )
        self.player.get_channel_connection_info.assert_called_once_with(
            guild_id=867344761970229258,
            channel_id=941028651057709057,
            timeout=2,
        )

    async def test_stop(self) -> None:
        self.mock_lavasnek_client.stop = AsyncMock()

        await self.player.stop(guild_id=867344761970229258)

        self.mock_lavasnek_client.stop.assert_called_once_with(867344761970229258)

    async def test_pause(self) -> None:
        self.mock_lavasnek_client.pause = AsyncMock()

        await self.player.pause(guild_id=867344761970229258)

        self.mock_lavasnek_client.pause.assert_called_once_with(867344761970229258)

    async def test_unpause(self) -> None:
        self.mock_lavasnek_client.resume = AsyncMock()

        await self.player.unpause(guild_id=867344761970229258)

        self.mock_lavasnek_client.resume.assert_called_once_with(867344761970229258)

    async def test_paused(self) -> None:
        self.mock_lavasnek_client.get_guild_node = AsyncMock(
            return_value=AsyncMock(**{"is_paused": True}),
        )
        result = await self.player.paused(guild_id=867344761970229258)
        self.assertTrue(result)

        # Test unknown guild
        with self.assertRaises(ValueError):
            self.mock_lavasnek_client.get_guild_node = AsyncMock(
                return_value=None,
            )
            await self.player.paused(guild_id=867344761970229258)

    async def test_leave(self) -> None:
        await self.player.leave(guild_id=867344761970229258)

        self.mock_bot.update_voice_state.assert_called_once_with(
            867344761970229258,
            None,
        )
        self.mock_lavasnek_client.wait_for_connection_info_remove.assert_called_once_with(
            867344761970229258,
        )

    async def test_play(self) -> None:
        track_mock = MagicMock()
        self.mock_lavasnek_client.play = MagicMock(
            **{"return_value.start": AsyncMock()}
        )

        # Test normal
        self.mock_lavasnek_client.get_tracks.return_value = MagicMock()
        tracks_result_mock = self.mock_lavasnek_client.get_tracks.return_value

        await self.player.play(
            guild_id=867344761970229258,
            track=track_mock,
        )

        self.mock_lavasnek_client.get_tracks.assert_called_once_with(
            track_mock.url,
        )
        self.mock_lavasnek_client.play.assert_called_once_with(
            guild_id=867344761970229258,
            track=tracks_result_mock.tracks[0],
        )
        self.mock_lavasnek_client.play.return_value\
            .start.assert_awaited_once_with()

        self.assertEqual(self.player._current_track, track_mock)


        # Test TracksNoFound
        self.mock_lavasnek_client.get_tracks.return_value = MagicMock(
            **{"tracks": []},
        )

        with self.assertRaises(TracksNoFound):
            await self.player.play(
                guild_id=867344761970229258,
                track=track_mock,
            )
