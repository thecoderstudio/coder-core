from enum import StrEnum
from typing import TypeVar

T = TypeVar("T")
SequentialCollection = list[T] | tuple[T, ...]


class UpperStrEnum(StrEnum):
    """StrEnum variant that auto-generates uppercase member values from names."""

    @staticmethod
    def _generate_next_value_(name: str, *args, **kwargs) -> str:
        return name.upper()
