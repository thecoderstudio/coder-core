import json
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import asdict, dataclass
from typing import Any, Callable, Self

from sqlalchemy import Column, and_, or_, text
from sqlalchemy.sql import ColumnElement, Select
from sqlalchemy.sql.expression import TextClause

from codercore.lib.collection import Direction
from codercore.types import SequentialCollection


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
        return str(asdict(self))

    def encode(self) -> bytes:
        return urlsafe_b64encode(self._json_dumps().encode())

    @classmethod
    def decode(cls, v: bytes) -> Self:
        return Cursor(**cls._json_loads(v))

    def _json_dumps(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def _json_loads(v: bytes) -> dict[str, Any]:
        return json.loads(urlsafe_b64decode(v).decode())


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


def _get_order_comparable(
    order_by: SequentialCollection[Column],
    order_direction: Direction,
    cursor: Cursor,
) -> list[bool]:
    return or_(
        _get_order_operator(column, order_direction, cursor.direction)(
            cursor.last_value[i]
        )
        for i, column in enumerate(order_by)
    )


def _is_tied_last_value(
    order_by: SequentialCollection[Column],
    last_value: SequentialCollection[Any],
) -> bool:
    return and_(column == last_value[i] for i, column in enumerate(order_by))


def _get_id_comparables(
    id_columns: SequentialCollection[Column], cursor: Cursor
) -> list[bool]:
    return or_(
        _get_pagination_operator(column, cursor.direction)(cursor.last_id[i])
        for i, column in enumerate(id_columns)
    )


def _paginate(
    statement: Select,
    id_columns: SequentialCollection[Column],
    cursor: Cursor,
    order_by: SequentialCollection[Column],
    order_direction: Direction,
) -> Select:
    return statement.where(
        or_(
            _get_order_comparable(order_by, order_direction, cursor),
            and_(
                _is_tied_last_value(order_by, cursor.last_value),
                _get_id_comparables(id_columns, cursor),
            ),
        )
    )


def _get_order_by_clauses(
    order_by: SequentialCollection[Column],
    order_direction: Direction,
) -> list[TextClause]:
    return [text(f"{column.name} {order_direction}") for column in order_by]


def _get_order_by_id_clauses(
    id_columns: SequentialCollection[Column],
) -> list[TextClause]:
    return [text(f"{column.name} asc") for column in id_columns]


def paginate(
    statement: Select,
    id_column: Column | SequentialCollection[Column],
    cursor: Cursor | None,
    order_by: Column | SequentialCollection[Column],
    order_direction: Direction,
    limit: int,
) -> Select:
    id_columns = id_column if isinstance(id_column, (list, tuple)) else (id_column,)
    if cursor:
        if not isinstance(order_by, (list, tuple)):
            order_by = (order_by,)
            cursor.last_value = (cursor.last_value,)
        statement = _paginate(
            statement,
            id_columns,
            cursor,
            order_by,
            order_direction,
        )
    elif not isinstance(order_by, (list, tuple)):
        order_by = (order_by,)
    statement = statement.order_by(
        *_get_order_by_clauses(order_by, order_direction),
        *_get_order_by_id_clauses(id_columns),
    ).limit(limit)
    return statement
