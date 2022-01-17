"""Abstract repositories."""

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from .model import (
        Guild,
        Member,
        Lang,
    )


class ABCGuildRepository(ABC):
    @abstractmethod
    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""

    @abstractmethod
    async def get(self, guild_id: int) -> Guild:
        """Get guild from DB."""

    @abstractmethod
    async def set_lang(self, lang: Lang) -> None:
        """Set guild lang."""


class ABCMemberRepository(ABC):
    @abstractmethod
    async def add(self, member: Member) -> None:
        """Add member to DB."""

    @abstractmethod
    async def get(self, member_id: int) -> Member:
        """Get member from DB."""
