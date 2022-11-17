from tests.db.models.sample import Sample


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


async def test_redis_connection(redis_connection):
    key = 'foo'
    value = b'bar'
    await redis_connection.set(key, value)
    assert await redis_connection.get(key) == value
