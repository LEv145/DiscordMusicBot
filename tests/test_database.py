from unittest import IsolatedAsyncioTestCase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.sql import (
    select as sql_select,
)

from models import (
    Member,
)
from repository import (
    MemberRepository,
)
from orm import start_mappers, metadata


class TestRepositories(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        start_mappers()

        engine = create_async_engine("sqlite+aiosqlite:///:memory:")

        async with engine.begin() as connect:
            await connect.run_sync(metadata.create_all)

        self.session: AsyncSession = sessionmaker(bind=engine, class_=AsyncSession)()

    async def asyncTearDown(self) -> None:
        clear_mappers()
        await self.session.close()

    async def test_member_repository(self) -> None:
        repository = MemberRepository(self.session)

        member_id = 501089151089770517
        base_member = Member(id=member_id)

        # Test add
        await repository.add(base_member)

        sql_result = await self.session.execute(sql_select(Member))

        self.assertEqual(base_member, sql_result.scalar())

        # Test get
        member = await repository.get(member_id)

        self.assertEqual(base_member, member)
