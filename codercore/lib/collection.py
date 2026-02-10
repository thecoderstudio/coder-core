from enum import StrEnum, auto


class Direction(StrEnum):
    """Sort direction for ordering and pagination."""

    ASC = auto()
    DESC = auto()
