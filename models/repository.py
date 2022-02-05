"""Repository."""

from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    from songbird.hikari import Voicebox
    from .abc_repository import ABCVoiceRepository


class DictVoiceRepository(ABCVoiceRepository):
    def __init__(self) -> None:
        self.__cache: dict[int, Voicebox] = {}

    async def add(self, id_: int, voice: Voicebox) -> None:
        """Add voicebox."""
        self.__cache[id_] = voice

    async def get(self, id_: int) -> Voicebox | None:
        """Get voicebox by id."""
        return self.__cache.get(id_)

    async def remove(self, id_: int) -> None:
        """Remove voicebox by id."""
        self.__cache.pop(id_, None)

