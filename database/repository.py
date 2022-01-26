"""Repositories."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.sql import (
    select as sql_select,
)

from .abc_repository import (
    ABCGuildRepository,
    ABCMemberRepository,
)
from .models import (
    Member,
    Guild,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class GuildRepository(ABCGuildRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""
        await self._session.add(guild)

    async def get(self, guild_id: int) -> Guild:
        """Get guild from DB."""
        result = await self._session.execute(
            sql_select(Guild).where(Guild.id == guild_id)
        )

        scalar: Guild = result.scalar()

        return scalar


class MemberRepository(ABCMemberRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, member: Member) -> None:
        """Add member to DB."""
        self._session.add(member)

    async def get(self, member_id: int) -> Member:
        """Get member from DB."""
        select = sql_select(Member)

        result = await self._session.execute(
            select.where(Member.id == member_id)
        )
        scalar: Member = result.scalar()

        return scalar
