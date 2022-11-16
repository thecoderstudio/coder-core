from __future__ import annotations

from functools import cache
from typing import Any, Awaitable, Optional, Union

from redis.asyncio import StrictRedis


@cache
def connection(
    host: str,
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None,
    default_ttl_in_seconds: Optional[int] = None,
) -> Redis:
    return Redis(
        host=host,
        port=port,
        db=db,
        password=password,
        default_ttl_in_seconds=default_ttl_in_seconds,
    )


class Redis(StrictRedis):
    default_ttl_in_seconds: Optional[int]

    def __init__(
        self,
        *args,
        default_ttl_in_seconds: Optional[int] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.default_ttl_in_seconds = default_ttl_in_seconds

    async def set(
        self,
        *args,
        ex: Optional[int] = None,
        **kwargs,
    ) -> Union[Awaitable, Any]:
        if not ex:
            ex = self.default_ttl_in_seconds
        await super().set(*args, ex=ex, **kwargs)
