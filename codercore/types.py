from enum import StrEnum


class UpperStrEnum(StrEnum):
    @classmethod
    def _generate_next_value_(cls, *args, **kwargs) -> str:
        return super()._generate_next_value_(*args, **kwargs).upper()
