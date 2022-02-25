from allocation.abс_repositories import ABCQueueRepository
from allocation.models import Track


class DictQueueRepository(ABCQueueRepository):
    def __init__(self) -> None:
        self._data: dict[int, Track] = {}

    async def check_is_empty(self, key: int) -> bool:
        """Check is queue empty."""

        return self._data.get(key, None) is not None

    async def get(self, key: int) -> Track:
        """Get track with wait."""
        ...

    async def get_nowait(self, key: int) -> Track | None:
        """Get track with without."""

        return self._data.get(key, None)

    async def put(self, key: int, track: Track) -> None:
        """Put track to queue with wait."""

        self._data[key] = track

    async def skip_to(self, n: int) -> None:
        """Skip the queue by `n`."""
        ...
