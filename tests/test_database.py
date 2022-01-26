from unittest import IsolatedAsyncioTestCase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.sql import (
    select as sql_select,
)

from database import (
    GuildRepository,
    MemberRepository,
    Guild,
    Member,
    Lang,
    SearchService,
    start_mappers,
    metadata,
)


class TestRepositories(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        start_mappers()

        engine = create_async_engine("sqlite+aiosqlite:///:memory:")

        async with engine.begin() as connect:
            await connect.run_sync(metadata.create_all)

        self.session: AsyncSession = sessionmaker(bind=engine, class_=AsyncSession)()

    async def asyncTearDown(self) -> None:
        await self.session.close()

    async def test_guild_add(self) -> None:
        repository = MemberRepository(self.session)

        member = Member(id=501089151089770517)
        await repository.add(Member(id=501089151089770517))

        sql_result = await self.session.execute(
            sql_select(Member).where(Member.id == 501089151089770517)
        )

        self.assertEqual(member, sql_result.scalar())

