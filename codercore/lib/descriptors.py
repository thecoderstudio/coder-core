from collections.abc import Callable


class classproperty[C, T]:
    """Class-level `property` decorator. Read-only."""

    _getter: Callable[[type[C]], T]

    def __init__(self, getter: Callable[[type[C]], T]) -> None:
        self._getter = getter

    def __get__(self, instance: C, owner: type[C] | None = None) -> T:
        return self._getter(owner if owner is not None else type(instance))
