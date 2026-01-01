from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine
from .settings import app_settings
from sqlmodel import SQLModel
from fastapi import Depends
from auth.models import User

engine = create_async_engine(app_settings.db_url, echo=app_settings.debug)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    session_instance = AsyncSession(engine, expire_on_commit=False)
    async with session_instance as session:
        yield session


SessionDep = Depends(get_session)
