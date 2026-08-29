from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config.settings import get_settings

settings = get_settings()


# ---------------------------------------------------------
# SQLAlchemy Base
# ---------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# Database URL
# ---------------------------------------------------------

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port,
    database=settings.postgres_db,
)


# ---------------------------------------------------------
# Async Engine
# ---------------------------------------------------------

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)


# ---------------------------------------------------------
# Async Session Factory
# ---------------------------------------------------------

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ---------------------------------------------------------
# FastAPI Database Dependency
# ---------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session