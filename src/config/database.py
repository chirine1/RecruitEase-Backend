from sqlalchemy.ext.asyncio import create_async_engine 
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from src.config.settings import Settings



Base = declarative_base()


engine = create_async_engine(
    url=Settings().DATABASE_URI, echo=True, future=True
)


async def get_session():
    async with AsyncSession(
        engine, expire_on_commit=False
    ) as session:
        yield session


