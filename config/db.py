from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from .settings import app_settings
from sqlmodel import SQLModel
from fastapi import Depends
from auth.models import User

engine = create_async_engine(app_settings.db_url, echo=app_settings.debug)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

session = get_session()
SessionType = Annotated[AsyncSession, Depends(get_session)]
