from collections.abc import AsyncIterator

from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

from codercore.db import get_connection_url, sessionmaker
from codercore.db.models import Base
from codercore.lib.redis import connection, Redis
from codercore.lib.settings import EnvSettings


def db_sessionmaker(
    user: str,
    password: str,
    host: str,
    worker_id: str,
    *args,
    **kwargs
) -> sqlalchemy_sessionmaker:
    connection_settings = {
        'user': user,
        'password': password,
        'host': host,
        'database': worker_id
    }

    sync_connection_url = get_connection_url('postgresql',
                                             **connection_settings)
    async_connection_url = get_connection_url('postgresql+asyncpg',
                                              **connection_settings)
    if not database_exists(sync_connection_url):
        create_database(sync_connection_url)
    return sessionmaker(async_connection_url, *args, **kwargs)


async def db_session(
    db_sessionmaker: sqlalchemy_sessionmaker
) -> AsyncIterator[Session]:
    async with db_sessionmaker() as session:
        async with session.bind.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with session.begin():
            yield session


async def redis_connection(worker_id: str) -> AsyncIterator[Redis]:
    redis = connection(db=int(worker_id[2:]), **EnvSettings.redis)
    yield redis
    await redis.close()
