from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.resources.database import async_session
from app.repositories import FarpostRepository


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_farpost_repository(session: AsyncSession = Depends(get_session)) -> FarpostRepository:
    return FarpostRepository(session)
