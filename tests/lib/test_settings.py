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


def test_env_settings_redis():
    assert EnvSettings.redis == {"host": "cache-test", "port": 6379}
