from orm import start_mappers

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DatabaseManager():
    """Class for database management."""

    def __init__(self, url: str) -> None:
        start_mappers()

        self.engine = create_async_engine(url)

        base_session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
        )

        self.session: AsyncSession = base_session_factory()

    async def close(self) -> None:
        await self.session.close()
