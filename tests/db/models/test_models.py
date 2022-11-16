import pytest
from sqlalchemy import Column, String

from codercore.db.models import Base


class BaseImpl(Base):
    __tablename__ = "base_impl"

    a = Column(String, primary_key=True)
    b = Column(String)

    def __hash__(self) -> int:
        return hash(hash(self.a) + hash(self.b))


def _create_base_impl_pair() -> tuple[Base, Base]:
    return BaseImpl(a="1", b="3"), BaseImpl(a="2", b="1")


def test_set_fields():
    base_impl = BaseImpl(a="1", b="2")
    base_impl.set_fields(b="3")

    assert base_impl.a == "1"
    assert base_impl.b == "3"


def test_base_hash_not_implemented():
    with pytest.raises(NotImplementedError):
        hash(Base())


def test_eq():
    base_impl, other_base_impl = _create_base_impl_pair()
    assert base_impl == base_impl
    assert (base_impl == other_base_impl) is False


def test_eq_incorrect_instance():
    base_impl = BaseImpl(a="1", b="3")
    assert (base_impl == 42) is False


def test_ne():
    base_impl, other_base_impl = _create_base_impl_pair()
    assert base_impl != other_base_impl
    assert (base_impl != base_impl) is False


def test_ne_incorrect_instance():
    base_impl = BaseImpl(a="1", b="3")
    assert base_impl != 42
