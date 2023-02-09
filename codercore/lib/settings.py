import os

from codercore.db import get_connection_url


class EnvSettings:
    @classmethod
    @property
    def database(cls) -> dict[str, str]:
        base = {
            "user": os.environ["POSTGRES_USER"],
            "database": os.environ["POSTGRES_DB"],
        }
        if os.environ.get("POSTGRES_USE_SQL_CONNECTOR", False):
            return {
                "instance_connection_name": os.environ[
                    "POSTGRES_INSTANCE_CONNECTION_NAME"
                ],
                **base,
            }
        else:
            return {
                "password": os.environ["POSTGRES_PASSWORD"],
                "host": os.environ["POSTGRES_HOST"],
                **base,
            }

    @classmethod
    @property
    def database_connection_url(cls) -> str:
        return get_connection_url("postgresql+asyncpg", **cls.database)

    @classmethod
    @property
    def redis(cls) -> dict:
        return {
            "host": os.environ["REDIS_HOST"],
            "port": int(os.environ["REDIS_PORT"]),
        }
