"""Repositories."""

from .abc_repository import (
    ABCGuildRepository,
    ABCMemberRepository,
)

from .model import (
    Member,
    Guild,
    Lang,
)


class GuildRepository(ABCGuildRepository):
    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""

    async def get(self, guild_id: int):
        """Get guild from DB."""

    async def set_lang(self, lang: Lang) -> None:
        """Set guild lang."""


class MemberRepository(ABCMemberRepository):
    async def add(self, member: Member) -> None:
        """Add member to DB."""

    async def get(self, member_id: int) -> Member:
        """Get member from DB."""
