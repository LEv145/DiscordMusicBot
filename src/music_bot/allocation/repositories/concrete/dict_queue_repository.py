import typing
import asyncio
from collections import defaultdict

from ..abstract import ABCQueueRepository
from ..models import Track


class DictQueueRepository(ABCQueueRepository):
    def __init__(self) -> None:
        self._data: defaultdict[int, asyncio.Queue[Track]] = defaultdict(asyncio.Queue)

    async def check_is_empty(self, key: int) -> bool:
        """Check is queue empty."""
        table = self._data[key]

        return table.empty()

    async def get(self, key: int) -> Track:
        """Get track with wait."""
        table = self._data[key]

        return await table.get()

    async def get_nowait(self, key: int) -> Track | None:
        """Get track with without."""
        table = self._data[key]

        try:
            return table.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def put(self, key: int, track: Track) -> None:
        """Put track to queue with wait."""
        table = self._data[key]

        await table.put(track)

    async def put_many(self, key: int, tracks: typing.Iterator[Track]) -> None:
        table = self._data[key]

        for track in tracks:
            await table.put(track)

    async def skip_to(self, n: int) -> None:
        """Skip the queue by `n`."""
        ...
