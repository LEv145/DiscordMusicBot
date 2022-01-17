from orm import start_mappers

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session


class Database():
    def __init__(self, url: str):
        start_mappers()

        self.engine = create_async_engine(url)

        base_session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
        )

        self.session: AsyncSession = base_session_factory()

    async def close(self):
        await self.session.close()

