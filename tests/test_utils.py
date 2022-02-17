import time
from unittest import IsolatedAsyncioTestCase

from music_bot.utils.general import async_wait_until


class TestUtils(IsolatedAsyncioTestCase):
    async def test_async_wait_until(self) -> None:
        async def test_function(key: int) -> int:
            return key

        # Test Timeout
        start_time = time.time()
        with self.assertRaises(TimeoutError):
            await async_wait_until(
                lambda x: x == 1,
                test_function,
                timeout=3,
                period=1,
                key=0,
            )
        self.assertTrue(2.5 <= time.time() - start_time <= 3.5)

        # Test result
        self.assertEqual(
            await async_wait_until(
                lambda x: x == 1,
                test_function,
                timeout=3,
                period=1,
                key=1,
            ),
            1,
        )
