import os
from collections.abc import AsyncIterator

from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker as db_sessionmaker

from codercore.db.models import Base
from codercore.test.fixtures import (
    DBSession as DBSession_,
    async_db_connection_url as async_db_connection_url_,
    clean_up_for_worker as clean_up_for_worker_,
    connection_settings as connection_settings_,
    db_session as db_session_,
    redis_connection as redis_connection_,
    redis_connection_maker as redis_connection_maker,
    sync_db_connection_url as sync_db_connection_url_,
)

sync_db_connection_url = fixture(sync_db_connection_url_, scope="session")
async_db_connection_url = fixture(async_db_connection_url_, scope="session")
DBSession = fixture(DBSession_)
redis_connection = fixture(redis_connection_)
clean_up_for_worker = fixture(clean_up_for_worker_, scope="session", autouse=True)
redis_connection_maker = fixture(redis_connection_maker)


@fixture(scope="session")
def connection_settings(worker_id: str) -> dict[str, str]:
    return connection_settings_(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        worker_id,
    )


@fixture
def sessionmaker(  # noqa
    sync_db_connection_url: str,
    async_db_connection_url: str,
) -> db_sessionmaker:
    return DBSession_(
        sync_db_connection_url,
        async_db_connection_url,
        expire_on_commit=False,
    )


@fixture
async def db_session(
    sessionmaker: db_sessionmaker,
) -> AsyncIterator[AsyncSession]:  # noqa
    async for session in db_session_(sessionmaker, Base.metadata):
        yield session
