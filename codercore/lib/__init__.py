from typing import Any


def setattrs(obj: Any, **kwargs) -> None:
    for key, value in kwargs.items():
        setattr(obj, key, value)
