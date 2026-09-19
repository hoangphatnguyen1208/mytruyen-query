from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

from fastapi import Depends
from typing import Annotated


engine = create_async_engine(
    settings.POSTGRES_URL,
    pool_size=5,
    max_overflow=5,
)

session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
