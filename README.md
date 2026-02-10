# Coder Core

Async-first Python utility library providing common infrastructure for backend services.

## Features

- **Database** — Async PostgreSQL session management via SQLAlchemy 2.0 + asyncpg, with Google Cloud SQL connector support
- **Cursor-based pagination** — Keyset pagination for SQLAlchemy queries with multi-column ordering and composite IDs
- **Redis** — Connection factory with TTL defaults and a `@cache` decorator for transparent async caching
- **Aggregation** — Query mixins for grouped and date-bucketed aggregations (year through second precision)
- **Password hashing** — bcrypt utilities for hashing and verification
- **HTTP** — Async context manager for validating third-party API responses
- **Settings** — Environment-variable-based configuration loader for database and Redis
- **Test utilities** — Reusable pytest fixtures for async database sessions, Redis connections, and Pydantic validation helpers

## Installation

```bash
pip install codercore
```

## Quick Start

### Database Sessions

```python
from codercore.db import sessionmaker, get_connection_url

url = get_connection_url("postgresql+asyncpg", "user", "pass", "localhost", "mydb")
Session = sessionmaker(url)

async with Session() as session:
    result = await session.execute(...)
```

### Cursor-Based Pagination

```python
from codercore.db.pagination import paginate, Cursor
from codercore.lib.collection import Direction

statement = paginate(
    select(User),
    id_column=User.id,
    cursor=Cursor.decode(cursor_token) if cursor_token else None,
    order_by=User.created_at,
    order_direction=Direction.DESC,
    limit=20,
)
```

### Redis Caching

```python
from codercore.lib.redis import connection, cache

redis = connection(host="localhost", port=6379, default_ttl_in_seconds=300)

@cache(key=lambda user_id: f"user:{user_id}", ex=60)
async def get_user(user_id: str) -> str:
    ...
```

### Password Hashing

```python
from codercore.lib.hash import bcrypt_hash, bcrypt_check_plaintext_equals_hash

hashed, salt = bcrypt_hash("my_password")
is_valid = bcrypt_check_plaintext_equals_hash("my_password", hashed, salt)
```

## Requirements

- Python 3.12+
- PostgreSQL 15+ (required by `codercore.db`)
- Redis 7+ (required by `codercore.lib.redis`)

Modules such as `codercore.lib.hash`, `codercore.lib.http`, and `codercore.lib.aggregation` can be used independently without PostgreSQL or Redis.

## Documentation

Build and serve the API reference locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

Then visit `http://127.0.0.1:8000`. To build static HTML:

```bash
mkdocs build
```

## Development

```bash
pip install -e ".[test,dev]"
```

### Running Tests

Tests run against real PostgreSQL and Redis instances via Docker Compose:

```bash
docker compose -f test-compose.yml up --build
```

### Linting

This project uses [pre-commit](https://pre-commit.com/) for linting:

```bash
pre-commit install
pre-commit run --all-files
```

## License

[Apache-2.0](LICENSE)
