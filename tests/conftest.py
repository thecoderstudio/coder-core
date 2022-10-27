import os
from collections.abc import Iterator

from pytest import fixture
from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

from codercore.db import get_connection_url, sessionmaker
from codercore.db.models import Base
from codercore.lib.redis import connection, Redis
from codercore.lib.settings import EnvSettings


@fixture
def db_sessionmaker(worker_id: str) -> sqlalchemy_sessionmaker:
    connection_settings = {
        'user': os.environ['POSTGRES_USER'],
        'password': os.environ['POSTGRES_PASSWORD'],
        'host': os.environ['POSTGRES_HOST'],
        'database': worker_id
    }

    sync_connection_url = get_connection_url('postgresql',
                                             **connection_settings)
    async_connection_url = get_connection_url('postgresql+asyncpg',
                                              **connection_settings)
    if not database_exists(sync_connection_url):
        create_database(sync_connection_url)
    return sessionmaker(async_connection_url)


@fixture
async def db_session(db_sessionmaker: sqlalchemy_sessionmaker) -> Iterator[Session]:
    async with db_sessionmaker() as session:
        async with session.bind.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.drop_all)
                yield session
            finally:
                await conn.run_sync(Base.metadata.create_all)


@fixture
async def redis_connection(worker_id: str) -> Redis:
    redis = connection(db=int(worker_id[2:]), **EnvSettings.redis)
    yield redis
    await redis.close()
