from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum, auto
from typing import Any, TypeVar

T = TypeVar("T", bound=dict[str, Any])


class DatePrecision(StrEnum):
    """Supported date truncation levels for aggregation queries."""

    year = auto()
    quarter = auto()
    month = auto()
    week = auto()
    day = auto()
    hour = auto()
    minute = auto()
    second = auto()


@dataclass
class AggregationParameters:
    """Parameters for controlling grouping in aggregation queries."""

    grouped_by: list[str] = field(default_factory=lambda: [])


@dataclass
class DatedAggregationParametersMixin:
    """Mixin adding date range and precision parameters to aggregation queries."""

    min_date: datetime | None = None
    max_date: datetime | None = None
    date_precision: DatePrecision | None = None
