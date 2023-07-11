from pytest import fixture
from sqlalchemy import Column, Integer, String

from codercore.db import Base, select
from codercore.db.pagination import Cursor
from codercore.lib.collection import Direction


class Example(Base):
    __tablename__ = "example"

    id = Column(String(), primary_key=True)
    value = Column(Integer(), nullable=False)

    def __hash__(self) -> int:
        return hash((self.id, self.value))

    def __repr__(self) -> str:
        return self.id


@fixture
def a() -> Example:
    return Example(id="A", value=2)


@fixture
def b() -> Example:
    return Example(id="B", value=2)


@fixture
def c() -> Example:
    return Example(id="C", value=1)


@fixture(autouse=True)
async def commit_examples(db_session, a, b, c):
    async with db_session.begin():
        db_session.add(a)
        db_session.add(b)
        db_session.add(c)


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
                    select(Example).paginate(
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
                    select(Example).paginate(
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
                    select(Example).paginate(
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
                    select(Example).paginate(
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
                    select(Example).paginate(
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


async def test_paginate_no_cursor(db_session, a, b, c):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    select(Example).paginate(
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


async def test_paginate_order_by_id_no_cursor(db_session, a, b, c):
    async with db_session:
        result = (
            (
                await db_session.execute(
                    select(Example).paginate(
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
