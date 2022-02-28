from __future__ import annotations

import typing
import abc

from ..models import Track


class ABCQueueRepository(abc.ABC):
    @abc.abstractmethod
    async def check_is_empty(self, key: int) -> bool:
        """Check is queue empty."""

    @abc.abstractmethod
    async def get(self, key: int) -> Track:
        """Get track with wait."""

    @abc.abstractmethod
    async def get_nowait(self, key: int) -> Track | None:
        """Get track with without."""

    @abc.abstractmethod
    async def put(self, key: int, track: Track) -> None:
        """Put track to queue with wait."""

    @abc.abstractmethod
    async def put_many(self, key: int, tracks: typing.Iterable[Track]) -> None:
        """Put many tracks to queue with wait."""

    @abc.abstractmethod
    async def skip_to(self, n: int) -> None:
        """Skip the queue by `n`."""
