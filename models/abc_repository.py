"""Abstract repositories."""  # FIXME: New path

from __future__ import annotations

import typing

from abc import ABC, abstractmethod


if typing.TYPE_CHECKING:
    from songbird.hikari import Voicebox


class ABCVoiceRepository(ABC):  # TODO: VoiceController
    # TODO: Abc for dict logic (1 obj by id)
    @abstractmethod
    async def add(self, id_: int, voice: Voicebox) -> None:
        """Add voicebox."""

    @abstractmethod
    async def get(self, id_: int) -> Voicebox | None:
        """Get voicebox by id."""

    @abstractmethod
    async def remove(self, id_: int) -> None:
        """Remove voicebox by id."""
