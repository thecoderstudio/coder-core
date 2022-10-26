from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker as sessionmaker_


@lru_cache(maxsize=1)
def sessionmaker(connection_url: str, *args, **kwargs) -> sessionmaker_:
    return sessionmaker(create_engine(connection_url), *args, **kwargs)


def init_sqlalchemy(connection_url: str) -> Engine:
    engine = create_engine(connection_url)
    return engine


def get_connection_url(driver: str, user: str, password: str, host: str,
                       database: str) -> str:
    return f"{driver}://{user}:{password}@{host}/{database}"
