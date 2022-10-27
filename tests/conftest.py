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
def db_sessionmaker(worker_id) -> sqlalchemy_sessionmaker:
    connection_url = get_connection_url(
        'postgresql',
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        worker_id
    )
    if not database_exists(connection_url):
        create_database(connection_url)
    return sessionmaker(connection_url)


@fixture
def db_session(db_sessionmaker: sqlalchemy_sessionmaker) -> Iterator[Session]:
    try:
        Base.metadata.create_all()
        with db_sessionmaker() as session:
            yield session
    finally:
        Base.metadata.drop_all()


@fixture
def redis_connection(worker_id) -> Redis:
    return connection(db=int(worker_id[2:]), **EnvSettings.redis)
