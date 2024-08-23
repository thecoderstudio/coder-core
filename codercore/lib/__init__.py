from typing import Any


def setattrs(obj: Any, exclude_none: bool = False, **kwargs) -> None:
    for key, value in kwargs.items():
        if exclude_none and value is None:
            continue
        setattr(obj, key, value)
