from functools import lru_cache
from typing import Optional

from redis import StrictRedis


@lru_cache(maxsize=1)
def connection(
    host: str,
    port: int = 6379,
    db: int = 0,
    password: Optional[str] = None
) -> StrictRedis:
    return StrictRedis(host=host, port=port, db=db, password=password)
