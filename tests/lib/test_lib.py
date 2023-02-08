from codercore.lib import setattrs


class Sample:
    a: int = 1
    b: str = "b"
    c: bool = True


def test_set_attrs():
    sample = Sample()
    setattrs(sample, a=2, c=False)
    assert sample.a == 2
    assert sample.b == "b"
    assert not sample.c
