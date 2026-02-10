import json
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import asdict, dataclass
from typing import Any, Callable, Self

from sqlalchemy import (
    ColumnElement,
    Select,
    UnaryExpression,
    and_,
    asc,
    desc,
    or_,
)

from codercore.lib.collection import Direction
from codercore.types import SequentialCollection


@dataclass
class Cursor:
    """Pagination cursor encoding the last seen ID, value, and direction.

    Supports JSON (de)serialization via base64-encoded tokens.
    """

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
        return cls(**cls._json_loads(v))

    def _json_dumps(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def _json_loads(v: bytes) -> dict[str, Any]:
        return json.loads(urlsafe_b64decode(v).decode())


def _get_pagination_operator(
    column: ColumnElement, direction: Direction
) -> Callable[[object], ColumnElement[bool]]:
    return column.__gt__ if direction == Direction.ASC else column.__lt__


def _get_order_operator(
    column: ColumnElement,
    order_direction: Direction,
    pagination_direction: Direction,
) -> Callable[[object], ColumnElement[bool]]:
    if order_direction == pagination_direction:
        return column.__gt__
    else:
        return column.__lt__


def _get_order_comparable(
    order_by: SequentialCollection[ColumnElement],
    order_direction: Direction,
    cursor: Cursor,
) -> ColumnElement[bool]:
    return or_(
        *(
            _get_order_operator(column, order_direction, cursor.direction)(
                cursor.last_value[i]
            )
            for i, column in enumerate(order_by)
        )
    )


def _is_tied_last_value(
    order_by: SequentialCollection[ColumnElement],
    last_value: SequentialCollection[Any],
) -> ColumnElement[bool]:
    return and_(*(column == last_value[i] for i, column in enumerate(order_by)))


def _get_id_comparables(
    id_columns: SequentialCollection[ColumnElement], cursor: Cursor
) -> ColumnElement[bool]:
    return or_(
        *(
            _get_pagination_operator(column, cursor.direction)(cursor.last_id[i])
            for i, column in enumerate(id_columns)
        )
    )


def _paginate(
    statement: Select,
    id_columns: SequentialCollection[ColumnElement],
    cursor: Cursor,
    order_by: SequentialCollection[ColumnElement],
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
    order_by: SequentialCollection[ColumnElement],
    order_direction: Direction,
) -> list[UnaryExpression]:
    expression = desc if order_direction == Direction.DESC else asc
    return [expression(column) for column in order_by]


def _get_order_by_id_clauses(
    id_columns: SequentialCollection[ColumnElement],
) -> list[UnaryExpression]:
    return [asc(column) for column in id_columns]


def paginate(
    statement: Select,
    id_column: ColumnElement | SequentialCollection[ColumnElement],
    cursor: Cursor | None,
    order_by: ColumnElement | SequentialCollection[ColumnElement],
    order_direction: Direction,
    limit: int,
) -> Select:
    """Add cursor-based WHERE, ORDER BY, and LIMIT clauses to a SELECT statement."""
    id_columns: SequentialCollection[ColumnElement]
    if isinstance(id_column, (list, tuple)):
        id_columns = id_column  # ty: ignore[invalid-assignment]
    else:
        id_columns = (id_column,)

    order_by_seq: SequentialCollection[ColumnElement]
    if isinstance(order_by, (list, tuple)):
        order_by_seq = order_by  # ty: ignore[invalid-assignment]
    else:
        order_by_seq = (order_by,)
    if cursor:
        if not isinstance(order_by, (list, tuple)):
            cursor.last_value = (cursor.last_value,)
        if not isinstance(id_column, (list, tuple)):
            cursor.last_id = (cursor.last_id,)
        statement = _paginate(
            statement,
            id_columns,
            cursor,
            order_by_seq,
            order_direction,
        )
    statement = statement.order_by(
        *_get_order_by_clauses(order_by_seq, order_direction),
        *_get_order_by_id_clauses(id_columns),
    ).limit(limit)
    return statement
