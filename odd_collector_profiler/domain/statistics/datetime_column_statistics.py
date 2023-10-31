from datetime import datetime
from typing import List

import pytz
from odd_models.models import DataSetFieldStat, DateTimeFieldStat

from .column_statistic import ColumnStatistic


class DatetimeColumnStatistic(ColumnStatistic):
    def __init__(
        self,
        column_name: str,
        low_value: datetime,
        high_value: datetime,
        nulls_count: int,
        unique_count: int,
        tags: List[str] = None,
    ) -> None:
        super().__init__(column_name, tags)
        self.low_value = low_value
        self.high_value = high_value
        self.nulls_count = nulls_count
        self.unique_count = unique_count

    def to_odd(self) -> DataSetFieldStat:
        data_entity = super().to_odd()
        data_entity.datetime_stats = DateTimeFieldStat(
            low_value=self.low_value.replace(tzinfo=pytz.utc).isoformat(),
            high_value=self.high_value.replace(tzinfo=pytz.utc).isoformat(),
            nulls_count=self.nulls_count,
            unique_count=self.unique_count,
        )

        return data_entity
