import os

from sqlalchemy import text

from src.common.model import Base
from src.core.conf import BASE_PATH
from src.database import async_engine

SQL_DIR = os.path.join(BASE_PATH, 'sql')
SQL_INIT_PATH = os.path.join(SQL_DIR, 'init_db.sql')


async def init_table():
    """Create a database table"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        if not os.path.exists(SQL_INIT_PATH):
            return

        with open(SQL_INIT_PATH, 'r') as f:
            await conn.execute(text(f.read()))
