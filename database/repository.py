"""Repositories."""
# TODO: Tests

from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import (
    Select,
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


class GuildRepository(ABCGuildRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, guild: Guild) -> None:
        """Add guild to DB."""
        self._session.session.add(guild)

    async def get(self, guild_id: int) -> Guild:
        """Get guild from DB."""
        select: Select = sql_select(Guild)

        result: ChunkedIteratorResult = await self._session.execute(
            select.where(Guild.id == guild_id)
        )
        scalar: Guild = result.scalar()

        return scalar


class MemberRepository(ABCMemberRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, member: Member) -> None:
        """Add member to DB."""
        self._session.session.add(member)

    async def get(self, member_id: int) -> Member:
        """Get member from DB."""
        select: Select = sql_select(Guild)

        result: ChunkedIteratorResult = await self._session.execute(
            select.where(Member.id == member_id)
        )
        scalar: Member = result.scalar()

        return scalar
