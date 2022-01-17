from orm import start_mappers

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session


class Database():
    def __init__(self, url: str):
        session_factory = sessionmaker(
            bind=create_async_engine(url),
            class_=AsyncSession,
        )
        self.session = scoped_session(session_factory())

    async def init(self):
        start_mappers()

    async def close(self):
        await self.session.session_factory.close()

