from fastapi import Depends
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import session_factory

async def get_session():
    async with session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]