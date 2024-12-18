import sys

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.common.model import Base
from src.core.conf import settings
from src.utils.logs import log


def create_engine_and_session(url: str, *, echo: bool = False):
    try:
        # Database engine
        engine = create_async_engine(
            url,
            echo=echo,
            future=True,
            pool_pre_ping=True
        )
        # log.success('The database connection is successful')
    except Exception as e:
        log.error("❌ Database link failed {}", e)
        sys.exit()
    else:
        db_session = async_sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False
        )
        return engine, db_session


async_engine, async_db_session = create_engine_and_session(settings.APP.DB_URL, echo=settings.APP.DB_ECHO)


async def get_db() -> AsyncSession:
    """session generators"""
    session = async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()


# Session Annotated
CurrentSession = Annotated[AsyncSession, Depends(get_db)]


async def create_table():
    """Create a database table"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)