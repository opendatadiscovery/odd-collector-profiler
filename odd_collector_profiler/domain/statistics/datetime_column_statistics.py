from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from odd_models.models import DataSetFieldStat, DateTimeFieldStat

from .column_statistic import ColumnStatistic


@dataclass
class DatetimeColumnStatistic(ColumnStatistic):
    low_value: datetime
    high_value: datetime
    mean_value: Optional[int]
    median_value: Optional[int]
    nulls_count: int
    unique_count: int

    def to_odd(self, oddrn: str) -> DataSetFieldStat:
        return DataSetFieldStat(
            tags=[],
            field_oddrn=oddrn,
            datetime_stats=DateTimeFieldStat(
                low_value=self.low_value,
                high_value=self.high_value,
                mean_value=self.mean_value,
                median_value=self.median_value,
                nulls_count=self.nulls_count,
                unique_count=self.unique_count,
            ),
        )
