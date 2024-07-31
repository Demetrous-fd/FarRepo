from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import create_engine

from app.settings import settings

async_engine = create_async_engine(settings.database_dsn, echo=False)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

sync_engine = create_engine(settings.database_dsn, echo=False)
sync_session = sessionmaker(
    sync_engine, class_=Session, expire_on_commit=False
)
