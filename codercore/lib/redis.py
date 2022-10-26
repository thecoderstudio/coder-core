from functools import cache
from typing import Optional

from redis import StrictRedis


@cache
def connection(
    host: str,
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None
) -> StrictRedis:
    return StrictRedis(host=host, port=port, db=db, password=password)
