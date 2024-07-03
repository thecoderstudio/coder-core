from datetime import UTC, datetime

from codercore.db import Base
from codercore.db.aggregation import AggregationQuery, DatedAggregationQueryMixin
from codercore.lib.aggregation import (
    AggregationParameters,
    DatedAggregationParametersMixin,
    DatePrecision,
)


class ExampleParameters(AggregationParameters, DatedAggregationParametersMixin):
    def __init__(self, grouped_by: list[str] = [], *args, **kwargs) -> None:
        AggregationParameters.__init__(self, grouped_by)
        DatedAggregationParametersMixin.__init__(self, *args, **kwargs)


class ExampleQuery(AggregationQuery, DatedAggregationQueryMixin):
    order_by_column: str = "id"

    def __init__(self, model_class: Base, *args, **kwargs) -> None:
        self.model_class = model_class
        super().__init__(*args, **kwargs)

    def _expand_query(self, params: ExampleParameters) -> None:
        DatedAggregationQueryMixin._expand_query(self, params)
        AggregationQuery._expand_query(self, params)


async def test_aggregation_query_with_mixins(mocker):
    model_class_mock = mocker.MagicMock()
    model_class_mock.date = datetime.now(UTC)
    db_session_mock = mocker.AsyncMock()
    grouped_by = ["a", "b"]
    min_date = datetime.now(UTC)
    max_date = datetime.now(UTC)
    date_precision = DatePrecision.year
    params = ExampleParameters(
        grouped_by=grouped_by,
        min_date=min_date,
        max_date=max_date,
        date_precision=date_precision,
    )
    query = ExampleQuery(model_class_mock, params)

    await query.execute(db_session_mock)

    assert query.select_args[0].name == "year"
    assert query.select_args[1].name == "a"
    assert query.select_args[2].name == "b"
    assert query.where_args == (False, True)
    assert query.group_by_args == ("year", "a", "b")
