from __future__ import annotations

import copy
import os
from typing import Any

from codercore.db import get_connection_url
from codercore.lib.descriptors import classproperty
from codercore.lib.meta import Frozen


class EnvSettings(metaclass=Frozen):
    """Environment-variable-based configuration for database and Redis connections."""

    @classproperty
    def database(cls: type[EnvSettings]) -> dict[str, Any]:
        use_connector = bool(os.environ.get("POSTGRES_USE_SQL_CONNECTOR", False))
        base: dict[str, Any] = {
            "user": os.environ["POSTGRES_USER"],
            "database": os.environ["POSTGRES_DB"],
            "use_connector": use_connector,
        }
        if use_connector:
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

    @classproperty
    def database_connection_url(cls: type[EnvSettings]) -> str:
        db_settings: dict[str, Any] = copy.copy(cls.database)
        del db_settings["use_connector"]
        return get_connection_url("postgresql+asyncpg", **db_settings)

    @classproperty
    def redis(cls: type[EnvSettings]) -> dict[str, str | int]:
        return {
            "host": os.environ["REDIS_HOST"],
            "port": int(os.environ["REDIS_PORT"]),
        }
