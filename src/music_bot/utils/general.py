import typing
import time
import asyncio


ObjectType = typing.TypeVar("ObjectType")


async def async_wait_until(
    condition: typing.Callable[[ObjectType], bool],
    function: typing.Callable[..., typing.Awaitable[ObjectType]],
    timeout: int,
    period: float = 0.25,
    *args: typing.Any,
    **kwargs: typing.Any,
) -> ObjectType:
    """Asyncio wait until timeout expired."""
    end_time = time.time() + timeout
    while True:
        result = await function(*args, **kwargs)
        if condition(result):
            return result

        if time.time() >= end_time:
            break

        await asyncio.sleep(period)
    raise TimeoutExpired


class TimeoutExpired(Exception):
    """Timeout expired."""
