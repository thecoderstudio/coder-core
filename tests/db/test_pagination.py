import json
from base64 import urlsafe_b64encode
from dataclasses import asdict

from pytest import fixture
from sqlalchemy import Column, ColumnElement, Integer, String, select
from sqlalchemy.ext.hybrid import hybrid_property

from codercore.db import Base
from codercore.db.pagination import Cursor, paginate
from codercore.lib.collection import Direction


class Example(Base):
    __tablename__ = "example"

    id = Column(String(), primary_key=True)
    value = Column(Integer(), nullable=False)

    @hybrid_property
    def hybrid(self) -> int:
        return abs(self.value - 2)

    @hybrid.inplace.expression
    @classmethod
    def _hybrid_expression(cls) -> ColumnElement[int]:
        return (cls.value - 2) * -1

    def __hash__(self) -> int:
        return hash((self.id, self.value))

    def __repr__(self) -> str:
        return self.id


class Alternative(Base):
    __tablename__ = "alternative"

    id_a = Column(String(), primary_key=True)
    id_b = Column(Integer(), primary_key=True)
    value = Column(Integer(), nullable=False)

    def __hash__(self) -> int:
        return hash((self.id_a, self.id_b, self.value))

    def __repr__(self) -> str:
        return str((self.id_a, self.id_b))


@fixture
def a() -> Example:
    return Example(id="A", value=2)


@fixture
def b() -> Example:
    return Example(id="B", value=2)


@fixture
def c() -> Example:
    return Example(id="C", value=1)


@fixture
def d() -> Alternative:
    return Alternative(id_a="D", id_b=1, value=2)


@fixture
def e() -> Alternative:
    return Alternative(id_a="D", id_b=2, value=2)


@fixture
def f() -> Alternative:
    return Alternative(id_a="F", id_b=1, value=1)


@fixture(autouse=True)
async def commit_examples(db_session, a, b, c, d, e, f):
    async with db_session.begin():
        db_session.add(a)
        db_session.add(b)
        db_session.add(c)
        db_session.add(d)
        db_session.add(e)
        db_session.add(f)


async def test_paginate_forwards_order_desc(db_session, a, b, c):
    cursor = Cursor(
        last_id=a.id,
        last_value=a.value,
        direction=Direction.ASC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=cursor,
                        order_by=Example.value,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [b, c]


async def test_paginate_forwards_order_by_hybrid_property(db_session, a, b, c):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=None,
                        order_by=Example.hybrid,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [c, a, b]


async def test_paginate_alt_forwards_order_desc(db_session, d, e, f):
    cursor = Cursor(
        last_id=(d.id_a, d.id_b),
        last_value=d.value,
        direction=Direction.ASC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=cursor,
                        order_by=Alternative.value,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [e, f]


async def test_paginate_backwards_order_desc(db_session, a, b, c):
    cursor = Cursor(
        last_id=c.id,
        last_value=c.value,
        direction=Direction.DESC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=cursor,
                        order_by=Example.value,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [a, b]


async def test_paginate_alt_backwards_order_desc(db_session, d, e, f):
    cursor = Cursor(
        last_id=(f.id_a, f.id_b),
        last_value=f.value,
        direction=Direction.DESC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=cursor,
                        order_by=Alternative.value,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [d, e]


async def test_paginate_forwards_order_asc(db_session, a, b, c):
    cursor = Cursor(
        last_id=c.id,
        last_value=c.value,
        direction=Direction.ASC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=cursor,
                        order_by=Example.value,
                        order_direction=Direction.ASC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [a, b]


async def test_paginate_alt_forwards_order_asc(db_session, d, e, f):
    cursor = Cursor(
        last_id=(f.id_a, f.id_b),
        last_value=f.value,
        direction=Direction.ASC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=cursor,
                        order_by=Alternative.value,
                        order_direction=Direction.ASC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [d, e]


async def test_paginate_backwards_order_asc(db_session, a, b, c):
    cursor = Cursor(
        last_id=b.id,
        last_value=b.value,
        direction=Direction.DESC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=cursor,
                        order_by=Example.value,
                        order_direction=Direction.ASC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [c, a]


async def test_paginate_alt_backwards_order_asc(db_session, d, e, f):
    cursor = Cursor(
        last_id=(e.id_a, e.id_b),
        last_value=e.value,
        direction=Direction.DESC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=cursor,
                        order_by=Alternative.value,
                        order_direction=Direction.ASC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [f, d]


async def test_paginate_backwards_order_asc_limited(db_session, a, b, c):
    cursor = Cursor(
        last_id=b.id,
        last_value=b.value,
        direction=Direction.DESC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=cursor,
                        order_by=Example.value,
                        order_direction=Direction.ASC,
                        limit=1,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [c]


async def test_paginate_alt_backwards_order_asc_limited(db_session, d, e, f):
    cursor = Cursor(
        last_id=(e.id_a, e.id_b),
        last_value=e.value,
        direction=Direction.DESC,
    )
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=cursor,
                        order_by=Alternative.value,
                        order_direction=Direction.ASC,
                        limit=1,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [f]


async def test_paginate_no_cursor(db_session, a, b, c):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=None,
                        order_by=Example.value,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [a, b, c]


async def test_paginate_alt_no_cursor(db_session, d, e, f):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=None,
                        order_by=Alternative.value,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [d, e, f]


async def test_paginate_order_by_id_no_cursor(db_session, a, b, c):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Example),
                        id_column=Example.id,
                        cursor=None,
                        order_by=Example.id,
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [c, b, a]


async def test_paginate_alt_order_by_id_no_cursor(db_session, d, e, f):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    paginate(
                        select(Alternative),
                        id_column=(Alternative.id_a, Alternative.id_b),
                        cursor=None,
                        order_by=(Alternative.id_a, Alternative.id_b),
                        order_direction=Direction.DESC,
                        limit=3,
                    )
                )
            )
            .scalars()
            .all()
        )
    assert result == [f, e, d]


def test_cursor_bytes():
    cursor = Cursor(last_id="A", last_value=1, direction="asc")
    assert bytes(cursor) == cursor.encode()


def test_cursor_str():
    cursor = Cursor(last_id="A", last_value=1, direction="asc")
    assert str(cursor) == cursor.encode().decode()


def test_cursor_repr():
    cursor = Cursor(last_id="A", last_value=1, direction="asc")
    assert repr(cursor) == str(
        {
            "last_id": cursor.last_id,
            "last_value": cursor.last_value,
            "direction": cursor.direction,
        }
    )


def test_cursor_encode():
    cursor = Cursor(last_id="A", last_value=1, direction="asc")
    expected_bytes = urlsafe_b64encode(json.dumps(asdict(cursor)).encode())
    assert cursor.encode() == expected_bytes


def test_cursor_decode():
    cursor = Cursor(last_id="A", last_value=1, direction="asc")
    assert cursor.decode(cursor.encode()) == cursor
