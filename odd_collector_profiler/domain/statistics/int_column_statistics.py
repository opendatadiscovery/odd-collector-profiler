from dataclasses import dataclass
from typing import Optional

from odd_models.models import DataSetFieldStat, IntegerFieldStat

from .column_statistic import ColumnStatistic


@dataclass
class IntColumnStatistic(ColumnStatistic):
    low_value: int
    high_value: int
    mean_value: Optional[int]
    median_value: Optional[int]
    nulls_count: int
    unique_count: int

    def to_odd(self, oddrn: str) -> DataSetFieldStat:
        return DataSetFieldStat(
            tags=[],
            field_oddrn=oddrn,
            integer_stats=IntegerFieldStat(
                low_value=self.low_value,
                high_value=self.high_value,
                mean_value=self.mean_value,
                median_value=self.median_value,
                nulls_count=self.nulls_count,
                unique_count=self.unique_count,
            ),
        )
