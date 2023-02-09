from functools import cache
from typing import Callable, Optional, Type

from asyncpg.connection import Connection
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session as Session_, sessionmaker as sessionmaker_
from sqlalchemy.pool import Pool

from codercore.db.models import Base


@cache
def Session(connection_url: str) -> Session_:  # noqa
    return sessionmaker(connection_url)()


@cache
def sessionmaker(
    connection_url: str,
    *args,
    creator: Callable | None = None,
    poolclass: Optional[Type[Pool]] = None,
    **kwargs,
) -> sessionmaker_:
    engine_kwargs = {}
    if creator:
        engine_kwargs["creator"] = creator
    engine = create_async_engine(connection_url, poolclass=poolclass, **engine_kwargs)
    Base.metadata.bind = engine
    return sessionmaker_(engine, *args, class_=AsyncSession, **kwargs)


def get_connection_url(
    driver: str, user: str, password: str, host: str, database: str
) -> str:
    return f"{driver}://{user}:{password}@{host}/{database}"


def get_connection_with_auto_iam_creator(
    instance_connection_name: str,
    user: str,
    database: str,
) -> Callable[[], Connection]:
    connector = Connector()

    def creator() -> Connection:
        return connector.connect(
            instance_connection_name,
            "asyncpg",
            user=user,
            db=database,
            enable_iam_auth=True,
            ip_type=IPTypes.PUBLIC,
        )

    return creator
