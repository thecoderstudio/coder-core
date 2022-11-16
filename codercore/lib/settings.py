import os

from codercore.db import get_connection_url


class EnvSettings:
    @classmethod
    @property
    def database_connection_url(cls) -> str:
        return get_connection_url(
            "postgresql+asyncpg",
            os.environ["POSTGRES_USER"],
            os.environ["POSTGRES_PASSWORD"],
            os.environ["POSTGRES_HOST"],
            os.environ["POSTGRES_DB"],
        )

    @classmethod
    @property
    def redis(cls) -> dict:
        return {
            "host": os.environ["REDIS_HOST"],
            "port": int(os.environ["REDIS_PORT"]),
        }
