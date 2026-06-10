from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable

from pytest import FixtureRequest
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker as sessionmaker_
from sqlalchemy.pool import NullPool, Pool
from sqlalchemy_utils import create_database, database_exists, drop_database

from codercore.db import get_connection_url, sessionmaker
from codercore.db.models import Base
from codercore.lib.redis import Redis, connection
from codercore.lib.settings import EnvSettings


def connection_settings(
    user: str,
    password: str,
    host: str,
    database: str,
) -> dict[str, str]:
    """Build a database connection settings dict from given individual parameters."""
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
    poolclass: type[Pool] = NullPool,
    **kwargs,
) -> sessionmaker_:
    """Creates an (async) sessionmaker, creating the database if it doesn't exist."""
    if not database_exists(sync_db_connection_url):
        create_database(sync_db_connection_url)
    return sessionmaker(async_db_connection_url, *args, poolclass=poolclass, **kwargs)


async def db_session(
    DBSession: sessionmaker_,  # noqa
    metadata: MetaData = Base.metadata,  # ty: ignore[unresolved-attribute]
) -> AsyncIterator[AsyncSession]:
    """Yield a test database session.

    Creates tables on entry and drops them on exit.
    """
    async with DBSession() as session:
        try:
            async with session.bind.begin() as conn:
                await conn.run_sync(metadata.create_all)
            yield session
        finally:
            async with session.bind.begin() as conn:
                await conn.run_sync(metadata.drop_all)


def clean_up_for_worker(request: FixtureRequest, sync_db_connection_url: str) -> None:
    """Register a finalizer that drops the test database after the worker."""

    def cleanup():
        if not database_exists(sync_db_connection_url):
            return

        drop_database(sync_db_connection_url)

    request.addfinalizer(cleanup)


@asynccontextmanager
async def _redis_connection_maker(
    worker_id: str,
) -> AsyncIterator[Redis]:
    async def redis_connection() -> Redis:
        return connection.__wrapped__(
            db=int(worker_id[2:]),
            **EnvSettings.redis,  # ty: ignore[invalid-argument-type]
        )

    try:
        conn = await redis_connection()
        yield conn
    finally:
        await conn.flushdb()
        await conn.aclose()


async def redis_connection_maker(
    worker_id: str,
) -> Callable[[str], AbstractAsyncContextManager[Redis]]:
    return _redis_connection_maker


async def redis_connection(
    redis_connection_maker: Callable[[str], AbstractAsyncContextManager[Redis]],
    worker_id: str,
) -> Redis:
    async with redis_connection_maker(worker_id) as conn:
        return conn
