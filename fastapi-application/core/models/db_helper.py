from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from core.config import settings


class DatabaseHelper:
    def __init__(self,
                 url:str,
                 echo:bool=False,
                 pool_size:int = 50,
                 max_overflow:int = 50
                 ):

        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            max_overflow=max_overflow,
            pool_size = pool_size
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # to perform "session.commit" action
            autocommit=False,
            expire_on_commit=False
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session

db_helper = DatabaseHelper(
    url=str(settings.db.url))


