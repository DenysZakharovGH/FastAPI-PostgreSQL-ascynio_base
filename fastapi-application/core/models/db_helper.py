from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession, async_scoped_session,
)

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False) -> None:

        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # get current session + control async with
    # "scopefunc=current_task" that that work belongs to current task
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory= self.session_factory,
            scopefunc=current_task
        )
        return session


    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session




db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=True,
)