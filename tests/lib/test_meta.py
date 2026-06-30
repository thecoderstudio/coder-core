import pytest

from codercore.lib.meta import Frozen


class Foo(metaclass=Frozen):
    bar = "bar"


def test_frozen_setattr_raises():
    with pytest.raises(AttributeError):
        Foo.bar = "foo"
    assert Foo.bar == "bar"
