from functools import cache
from typing import Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker as sessionmaker_, Session as Session_
from sqlalchemy.pool import Pool

from codercore.db.models import Base


@cache
def Session(connection_url: str) -> Session_:  # noqa
    return sessionmaker(connection_url)()


@cache
def sessionmaker(
    connection_url: str,
    *args,
    poolclass: Optional[Type[Pool]] = None,
    **kwargs,
) -> sessionmaker_:
    engine = create_async_engine(connection_url, poolclass=poolclass)
    Base.metadata.bind = engine
    return sessionmaker_(engine, *args, class_=AsyncSession, **kwargs)


def get_connection_url(
    driver: str, user: str, password: str, host: str, database: str
) -> str:
    return f"{driver}://{user}:{password}@{host}/{database}"
