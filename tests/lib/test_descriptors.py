import pytest

from codercore.lib.descriptors import classproperty


class Foo:
    @classproperty
    def bar(cls) -> str:
        return "bar"


def test_classproperty_get_on_class():
    assert Foo.bar == "bar"


def test_classproperty_get_on_class_not_found():
    with pytest.raises(AttributeError):
        Foo.foo


def test_classproperty_get_on_instance():
    assert Foo().bar == "bar"


def test_classproperty_get_on_instance_not_found():
    with pytest.raises(AttributeError):
        Foo().foo
