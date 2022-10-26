from pytest import fixture
from sqlalchemy_utils import database_exists, create_database

from codercore.db import sessionmaker
from codercore.db.models import Base
from codercore.lib.settings import EnvSettings


@fixture(scope='session')
def db_sessionmaker():
    connection_url = EnvSettings.database_connection_url
    if not database_exists(connection_url):
        create_database(connection_url)
    return sessionmaker(connection_url)


@fixture
def db_session(db_sessionmaker):
    try:
        Base.metadata.create_all()
        with db_sessionmaker() as session:
            yield session
    finally:
        Base.metadata.drop_all()
