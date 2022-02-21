import unittest
from unittest.mock import MagicMock, Mock, AsyncMock


import lightbulb


class TestCommands(unittest.IsolatedAsyncioTestCase):
    async def test_play(self) -> None:
        play_command = MagicMock()

        # Test with empty queue
        plugin_mock = AsyncMock(spec=lightbulb.Plugin)
        plugin_mock.d.queue = MagicMock(**{"empty": Mock(return_value=True)})

        ctx_mock = AsyncMock(spec=lightbulb.Context)

        play_command(plugin_mock, ctx_mock)

        ctx_mock.respond.assert_awaited_once()  # Respond the queue is empty

        # Test with no empty queue
        plugin_mock = AsyncMock(spec=lightbulb.Plugin)
        plugin_mock.d.queue = MagicMock(
            **{
                "empty": Mock(return_value=False),
                "get_nowait": Mock(return_value=[MagicMock(), MagicMock()]),
            },
        )


