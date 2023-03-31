from codercore.db import get_connection_url
from codercore.test.fixtures import (
    async_db_connection_url,
    connection_settings,
    sync_db_connection_url,
)
from tests.db.models.sample import Sample


def test_connection_settings():
    data = {
        "user": "user",
        "password": "password",
        "host": "host",
        "database": "database",
    }
    assert connection_settings(**data) == data


def test_sync_db_connection_url(connection_settings):
    assert sync_db_connection_url(connection_settings) == get_connection_url(
        "postgresql",
        **connection_settings,
    )


def test_async_db_connection_url(connection_settings):
    assert async_db_connection_url(connection_settings) == get_connection_url(
        "postgresql+asyncpg", **connection_settings
    )


async def test_db_session_autobegin(db_session):
    sample = Sample(value="a")
    db_session.add(sample)
    await db_session.commit()


async def test_db_session_manual_transaction(db_session):
    sample = Sample(value="a")
    async with db_session.begin():
        db_session.add(sample)

    async with db_session.begin():
        persisted = await db_session.get(Sample, "a")
        initial_count = persisted.count
        persisted.count = 1

    async with db_session.begin():
        updated = await db_session.get(Sample, "a")
        updated_count = updated.count

    assert initial_count == 0
    assert updated_count == 1


async def test_redis_connection_maker(redis_connection_maker):
    redis_connection = await redis_connection_maker()
    key = "foo"
    value = b"bar"
    await redis_connection.set(key, value)
    assert await redis_connection.get(key) == value


async def test_redis_connection(redis_connection):
    key = "foo"
    value = b"bar"
    await redis_connection.set(key, value)
    assert await redis_connection.get(key) == value
