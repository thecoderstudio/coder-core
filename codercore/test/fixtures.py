from collections.abc import AsyncIterator

from pytest import FixtureRequest
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker as sessionmaker_
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import database_exists, create_database, drop_database

from codercore.db import get_connection_url, sessionmaker
from codercore.db.models import Base
from codercore.lib.redis import connection, Redis
from codercore.lib.settings import EnvSettings


def connection_settings(
    user: str,
    password: str,
    host: str,
    database: str,
) -> dict[str, str]:
    return {
        "user": user,
        "password": password,
        "host": host,
        "database": database,
    }


def sync_db_connection_url(connection_settings: dict[str, str]) -> str:
    return get_connection_url("postgresql", **connection_settings)


def async_db_connection_url(connection_settings: dict[str, str]) -> str:
    return get_connection_url("postgresql+asyncpg", **connection_settings)


def DBSession(  # noqa
    sync_db_connection_url: str,
    async_db_connection_url: str,
    *args,
    **kwargs,
) -> sessionmaker_:
    if not database_exists(sync_db_connection_url):
        create_database(sync_db_connection_url)
    return sessionmaker(async_db_connection_url, *args, poolclass=NullPool, **kwargs)


async def db_session(
    DBSession: sessionmaker_,  # noqa
    metadata: MetaData = Base.metadata,
) -> AsyncIterator[AsyncSession]:
    async with DBSession() as session:
        try:
            async with session.bind.begin() as conn:
                await conn.run_sync(metadata.create_all)
            yield session
        finally:
            async with session.bind.begin() as conn:
                await conn.run_sync(metadata.drop_all)


def clean_up_for_worker(request: FixtureRequest, sync_db_connection_url: str) -> None:
    def cleanup():
        if not database_exists(sync_db_connection_url):
            return

        drop_database(sync_db_connection_url)

    request.addfinalizer(cleanup)


async def redis_connection(worker_id: str) -> AsyncIterator[Redis]:
    redis = connection.__wrapped__(db=int(worker_id[2:]), **EnvSettings.redis)
    yield redis
    await redis.flushdb()
    await redis.close()
