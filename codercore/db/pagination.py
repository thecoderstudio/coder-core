from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import dataclass
from typing import Any, Callable, Self

import orjson
from sqlalchemy import Column, and_, or_, text
from sqlalchemy.sql import ColumnElement, Select

from codercore.lib.collection import Direction


@dataclass
class Cursor:
    last_id: Any
    last_value: Any
    direction: Direction

    def __bytes__(self) -> bytes:
        return self.encode()

    def __str__(self) -> str:
        return self.encode().decode()

    def __repr__(self) -> str:
        return str(self._dict())

    def _dict(self) -> dict[str, Any]:
        return {
            "last_id": self.last_id,
            "last_value": self.last_value,
            "direction": self.direction,
        }

    def encode(self) -> bytes:
        return urlsafe_b64encode(orjson.dumps(self._dict()))

    @staticmethod
    def decode(v: bytes) -> Self:
        return Cursor(**orjson.loads(urlsafe_b64decode(v)))


def _get_pagination_operator(
    column: Column, direction: Direction
) -> Callable[[ColumnElement], bool]:
    return column.__gt__ if direction == Direction.ASC else column.__lt__


def _get_order_operator(
    column: Column,
    order_direction: Direction,
    pagination_direction: Direction,
) -> Callable[[ColumnElement], bool]:
    if order_direction == pagination_direction:
        return column.__gt__
    else:
        return column.__lt__


def _paginate(
    statement: Select,
    id_column: Column,
    cursor: Cursor | None,
    order_by: Column,
    order_direction: Direction,
) -> Select:
    order_operator = _get_order_operator(order_by, order_direction, cursor.direction)
    pagination_operator = _get_pagination_operator(id_column, cursor.direction)
    return statement.where(
        or_(
            order_operator(cursor.last_value),
            and_(
                order_by == cursor.last_value,
                pagination_operator(cursor.last_id),
            ),
        )
    )


def paginate(
    statement: Select,
    id_column: Column,
    cursor: Cursor | None,
    order_by: Column,
    order_direction: Direction,
    limit: int,
) -> Select:
    if cursor:
        statement = _paginate(
            statement,
            id_column,
            cursor,
            order_by,
            order_direction,
        )
    statement = statement.order_by(
        text(f"{order_by.name} {order_direction}"),
        text(f"{id_column.name} asc"),
    ).limit(limit)
    return statement
