import os
from unittest.mock import patch

from codercore.lib.settings import EnvSettings


@patch.dict(
    os.environ,
    {
        "POSTGRES_USER": "user",
        "POSTGRES_PASSWORD": "password",
        "POSTGRES_HOST": "host",
        "POSTGRES_DB": "db",
    },
    clear=True,
)
def test_env_settings_database_connection_url():
    assert EnvSettings.database_connection_url == (
        "postgresql+asyncpg://user:password@host/db"
    )


@patch.dict(
    os.environ,
    {
        "POSTGRES_USER": "user",
        "POSTGRES_PASSWORD": "password",
        "POSTGRES_HOST": "host",
        "POSTGRES_DB": "db",
    },
    clear=True,
)
def test_env_settings_database():
    assert EnvSettings.database == {
        "user": "user",
        "password": "password",
        "host": "host",
        "database": "db",
        "use_connector": False,
    }


@patch.dict(
    os.environ,
    {
        "POSTGRES_USER": "user",
        "POSTGRES_DB": "db",
        "POSTGRES_USE_SQL_CONNECTOR": "True",
        "POSTGRES_INSTANCE_CONNECTION_NAME": "connection",
    },
    clear=True,
)
def test_env_settings_database_through_connector():
    assert EnvSettings.database == {
        "user": "user",
        "database": "db",
        "instance_connection_name": "connection",
        "use_connector": True,
    }


def test_env_settings_redis():
    assert EnvSettings.redis == {"host": "cache-test", "port": 6379}
