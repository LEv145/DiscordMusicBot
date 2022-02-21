import abc

from ..models import Track


class ABCQueueRepository(abc.ABC):
    async def check_is_empty(self) -> bool:
        """Check is queue empty."""

    async def get(self) -> Track:
        """Get track with wait."""

    async def get_nowait(self) -> Track | None:
        """Get track with without."""

    async def put(self, track: Track) -> None:
        """Put track to queue with wait."""

    async def skip_to(self, n: int) -> None:
        """Skip the queue by `n`."""
