"""Abstract repositories."""

from __future__ import annotations

import typing
from abc import ABC, abstractmethod


if typing.TYPE_CHECKING:
    from .models import (
        Guild,
        Member,
    )


class ABCGuildRepository(ABC):
    @abstractmethod
    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""

    @abstractmethod
    async def get(self, guild_id: int) -> Guild | None:
        """Get guild from DB."""


class ABCMemberRepository(ABC):
    @abstractmethod
    async def add(self, member: Member) -> None:
        """Add member to DB."""

    @abstractmethod
    async def get(self, member_id: int) -> Member | None:
        """Get member from DB."""
