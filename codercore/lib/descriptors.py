from collections.abc import Callable


class classproperty[T]:
    """Class-level `property` decorator. Read-only."""

    _getter: Callable[[type], T]

    def __init__(self, getter: Callable[[type], T]) -> None:
        self._getter = getter

    def __get__(self, instance: object, owner: type | None = None) -> T:
        return self._getter(owner if owner is not None else type(instance))
