import unittest
from unittest.mock import Mock, AsyncMock

from src.music_bot.extensions.music_extension import (
    StaticCommands,
    DefaultEmbed,
)
from allocation import (
    Track,
)

import lightbulb


class TestCommands(unittest.IsolatedAsyncioTestCase):
    async def test_play(self) -> None:
        play_command = StaticCommands.play_command


        # Test with empty queue
        plugin_mock = AsyncMock(
            lightbulb.Plugin,
            **{"d.queue.get_nowait": AsyncMock(return_value=None)},
        )
        ctx_mock = AsyncMock(
            lightbulb.Context,
            **{"command.plugin": plugin_mock},
        )

        await play_command(ctx_mock)

        ## Call once with `DefaultEmbed` type
        ctx_mock.respond.assert_awaited_once()
        self.assertIsInstance(ctx_mock.respond.await_args.args[0], DefaultEmbed)


        # Test with no empty queue
        # Test with empty queue
        plugin_mock = AsyncMock(
            lightbulb.Plugin,
            **{"d.queue.get_nowait": AsyncMock(return_value=[Mock(Track)])},
        )
        ctx_mock = AsyncMock(
            lightbulb.Context,
            **{"command.plugin": plugin_mock},
        )

        await play_command(ctx_mock)

        plugin_mock.d._lavasnek_client.play.assert_called_once()



