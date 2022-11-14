import os

from pytest import fixture
from sqlalchemy.orm import sessionmaker as sqlalchemy_sessionmaker

from codercore.test.fixtures import (
    db_sessionmaker as db_sessionmaker_,
    db_session as db_session_,
    redis_connection as redis_connection_
)

db_session = fixture(db_session_)
redis_connection = fixture(redis_connection_)


@fixture
def db_sessionmaker(worker_id: str) -> sqlalchemy_sessionmaker:
    return db_sessionmaker_(
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        worker_id
    )
