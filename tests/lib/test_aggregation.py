from datetime import UTC, datetime

import pytest

from codercore.lib.aggregation import (
    AggregationParameters,
    DatedAggregationParametersMixin,
    DatePrecision,
)


def test_aggregation_parameters_complete():
    grouped_by = ["a", "b"]
    params = AggregationParameters(grouped_by=grouped_by)
    assert params.grouped_by == grouped_by


def test_aggregation_parameters_defaults():
    params = AggregationParameters()
    assert params.grouped_by == []


@pytest.mark.parametrize("date_precision", tuple(DatePrecision))
def test_dated_aggregation_parameters_mixin_complete(date_precision):
    min_date = datetime.now(UTC)
    max_date = datetime.now(UTC)
    params = DatedAggregationParametersMixin(
        min_date=min_date,
        max_date=max_date,
        date_precision=date_precision,
    )
    assert params.min_date == min_date
    assert params.max_date == max_date
    assert params.date_precision == date_precision


def test_dated_aggregation_parameters_mixin_defaults():
    params = DatedAggregationParametersMixin()
    assert params.min_date is None
    assert params.max_date is None
    assert params.date_precision is None
