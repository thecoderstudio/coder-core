import os
from collections.abc import AsyncIterator

from pytest import fixture
from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker, Session

from codercore.lib.redis import Redis
from codercore.test.fixtures import (
    db_sessionmaker as db_sessionmaker_,
    db_session as db_session_,
    redis_connection as redis_connection_
)


@fixture
def db_sessionmaker(worker_id: str) -> sqlalchemy_sessionmaker:
    return db_sessionmaker_(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        worker_id
    )


@fixture
async def db_session(
    db_sessionmaker: sqlalchemy_sessionmaker
) -> AsyncIterator[Session]:
    async for session in db_session_(db_sessionmaker):
        yield session


@fixture
async def redis_connection(worker_id: str) -> AsyncIterator[Redis]:
    async for connection in redis_connection_(worker_id):
        yield connection
