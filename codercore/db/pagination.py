from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy import Column, and_, or_, text
from sqlalchemy.sql import ColumnElement, Select

from codercore.lib.collection import Direction


@dataclass
class Cursor:
    last_id: Any
    last_value: Any
    direction: Direction


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
