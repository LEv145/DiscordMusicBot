import time
from unittest import IsolatedAsyncioTestCase

from music_bot.utils.asyncio import async_wait_until, TimeoutExpired


class TestUtils(IsolatedAsyncioTestCase):
    async def test_async_wait_until(self) -> None:
        async def test_function(key: int) -> int:
            return key

        # Test Timeout
        start_time = time.time()
        with self.assertRaises(TimeoutExpired):
            await async_wait_until(
                lambda x: x == 1,
                test_function,
                timeout=3,
                period=1,
                key=0,
            )
        self.assertTrue(2.5 <= time.time() - start_time <= 3.5)  # TODO: Better time tests

        # Test result
        self.assertEqual(
            await async_wait_until(
                lambda x: x == 1,
                test_function,
                timeout=0,
                key=1,
            ),
            1,
        )
