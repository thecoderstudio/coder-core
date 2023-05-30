from functools import cache
from typing import Callable, Optional, Type

from asyncpg.connection import Connection
from asyncstdlib.functools import cache as async_cache
from google.cloud.sql.connector import IPTypes, create_async_connector
from sqlalchemy import select as sa_select
from sqlalchemy.dialects.postgresql.asyncpg import (
    AsyncAdapt_asyncpg_connection,
    AsyncAdapt_asyncpg_dbapi,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session as Session_, sessionmaker as sessionmaker_
from sqlalchemy.pool import Pool
from sqlalchemy.sql import Select
from sqlalchemy.util import await_only

from codercore.db.models import Base
from codercore.db.pagination import paginate


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


@async_cache
async def get_connection_with_auto_iam_creator(
    instance_connection_name: str,
    user: str,
    database: str,
) -> Callable[[], Connection]:
    connector = await create_async_connector()

    def creator() -> AsyncAdapt_asyncpg_connection:
        connection = connector.connect_async(
            instance_connection_name,
            "asyncpg",
            user=user,
            db=database,
            enable_iam_auth=True,
            ip_type=IPTypes.PUBLIC,
        )
        return AsyncAdapt_asyncpg_connection(
            AsyncAdapt_asyncpg_dbapi(__import__("asyncpg")),
            await_only(connection),
        )

    return creator


def select(*args, **kwargs) -> Select:
    statement = sa_select(*args, **kwargs)
    statement.paginate = paginate.__get__(statement)
    return statement
