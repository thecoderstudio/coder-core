from typing import Never


class Frozen(type):
    """Metaclass that makes class attributes immutable."""

    def __setattr__(cls, name: str, value: object) -> Never:
        raise AttributeError(f"{cls.__name__}.{name} is immutable")
