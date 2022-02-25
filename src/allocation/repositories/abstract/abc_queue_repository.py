from __future__ import annotations

import typing
import abc


if typing.TYPE_CHECKING:
    from allocation.models import Track


class ABCQueueRepository(abc.ABC):
    async def check_is_empty(self, key: int) -> bool:
        """Check is queue empty."""

    async def get(self, key: int) -> Track:
        """Get track with wait."""

    async def get_nowait(self, key: int) -> Track | None:
        """Get track with without."""

    async def put(self, key: int, track: Track) -> None:
        """Put track to queue with wait."""

    async def skip_to(self, n: int) -> None:
        """Skip the queue by `n`."""
