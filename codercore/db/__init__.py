from functools import cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as sessionmaker_, Session as Session_

from codercore.db.models import Base


@cache
def Session(connection_url: str) -> Session_:  # noqa
    return sessionmaker(connection_url)()


@cache
def sessionmaker(connection_url: str, *args, **kwargs) -> sessionmaker_:
    engine = create_engine(connection_url)
    Base.metadata.bind = engine
    return sessionmaker_(engine, *args, **kwargs)


def get_connection_url(driver: str, user: str, password: str, host: str,
                       database: str) -> str:
    return f"{driver}://{user}:{password}@{host}/{database}"
