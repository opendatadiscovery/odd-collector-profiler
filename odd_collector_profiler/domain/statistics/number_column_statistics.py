from typing import List, Optional

from odd_models.models import DataSetFieldStat, NumberFieldStat

from .column_statistic import ColumnStatistic


class NumberColumnStatistic(ColumnStatistic):
    def __init__(
        self,
        column_name: str,
        low_value: float,
        high_value: float,
        mean_value: Optional[float],
        median_value: Optional[float],
        nulls_count: int,
        unique_count: int,
        tags: List[str] = None,
    ) -> None:
        super().__init__(column_name, tags)
        self.low_value = low_value
        self.high_value = high_value
        self.mean_value = mean_value
        self.median_value = median_value
        self.nulls_count = nulls_count
        self.unique_count = unique_count

    def to_odd(self, oddrn: str) -> DataSetFieldStat:
        data_entity = super().to_odd(oddrn)
        data_entity.number_stats = NumberFieldStat(
            low_value=self.low_value,
            high_value=self.high_value,
            mean_value=self.mean_value,
            median_value=self.median_value,
            nulls_count=self.nulls_count,
            unique_count=self.unique_count,
        )

        return data_entity
