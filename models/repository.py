"""Repository."""

from __future__ import annotations

import typing

from .abc_repository import ABCVoiceRepository


if typing.TYPE_CHECKING:
    from songbird.hikari import Voicebox


class DictVoiceRepository(ABCVoiceRepository):
    def __init__(self) -> None:
        self._cache: dict[int, Voicebox] = {}

    async def add(self, id_: int, voice: Voicebox) -> None:
        """Add voicebox."""
        if id_ not in self._cache:
            self._cache[id_] = voice

    async def get(self, id_: int) -> Voicebox | None:
        """Get voicebox by id."""
        return self._cache.get(id_)

    async def remove(self, id_: int) -> None:
        """Remove voicebox by id."""
        self._cache.pop(id_, None)

