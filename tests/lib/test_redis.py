from codercore.lib.redis import connection, Redis
from codercore.lib.settings import EnvSettings


def test_connection_cached():
    connection_1 = connection(**EnvSettings.redis)
    connection_2 = connection(**EnvSettings.redis)
    assert connection_1 is connection_2


def test_init_redis():
    default_ttl = 30
    redis = Redis(**EnvSettings.redis, default_ttl_in_seconds=default_ttl)
    assert redis.default_ttl_in_seconds == default_ttl


def test_redis_set_default_ex(redis_connection):
    key = 'test'
    default_ttl = 30
    redis_connection.default_ttl_in_seconds = default_ttl
    redis_connection.set(key, 'value')
    assert redis_connection.ttl(key) == default_ttl


def test_redis_set_given_ex(redis_connection):
    key = 'test'
    default_ttl = 30
    ttl = 25
    redis_connection.default_ttl_in_seconds = default_ttl
    redis_connection.set(key, 'value', ex=ttl)
    assert redis_connection.ttl(key) == ttl
