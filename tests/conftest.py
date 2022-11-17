import os

from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker

from codercore.test.fixtures import (
    db_session as db_session_,
    DBSession as DBSession_,
    redis_connection as redis_connection_,
)

db_session = fixture(db_session_)
redis_connection = fixture(redis_connection_)


@fixture
def DBSession(worker_id: str) -> AsyncSession:
    return DBSession_(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        worker_id,
    )
