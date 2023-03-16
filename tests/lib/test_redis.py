from codercore.lib.redis import Redis, cache, connection
from codercore.lib.settings import EnvSettings


def test_connection_cached():
    connection_1 = connection(**EnvSettings.redis)
    connection_2 = connection(**EnvSettings.redis)
    assert connection_1 is connection_2


def test_init_redis():
    default_ttl = 30
    redis = Redis(**EnvSettings.redis, default_ttl_in_seconds=default_ttl)
    assert redis.default_ttl_in_seconds == default_ttl


async def test_redis_set_default_ex(redis_connection):
    key = "test"
    default_ttl = 30
    redis_connection.default_ttl_in_seconds = default_ttl
    await redis_connection.set(key, "value")
    assert await redis_connection.ttl(key) == default_ttl


async def test_redis_set_given_ex(redis_connection):
    key = "test"
    default_ttl = 30
    ttl = 25
    redis_connection.default_ttl_in_seconds = default_ttl
    await redis_connection.set(key, "value", ex=ttl)
    assert await redis_connection.ttl(key) == ttl


async def test_cache(redis_connection):
    @cache("test", deserialize=int)
    async def sample(value: int) -> int:
        return value

    result = await sample(1, connection=redis_connection)
    assert await sample(2, connection=redis_connection) == result


async def test_cache_with_key_lambda(redis_connection):
    @cache(lambda value: f"test_{value}", deserialize=int)
    async def sample(value: int) -> int:
        return value

    await sample(1, connection=redis_connection)
    assert await sample(2, connection=redis_connection) == 2


async def test_cache_ex_set(mocker):
    key = "test"
    ex = 10
    connection_mock = mocker.AsyncMock()
    connection_mock.get.return_value = None

    @cache(key, ex)
    async def sample(value: int) -> int:
        return value

    await sample(1, connection=connection_mock)
    connection_mock.set.assert_awaited_once_with(key, 1, ex=ex)
