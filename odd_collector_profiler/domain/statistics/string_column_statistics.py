from typing import List

from odd_models.models import DataSetFieldStat, StringFieldStat

from .column_statistic import ColumnStatistic


class StringColumnStatistic(ColumnStatistic):
    def __init__(
        self,
        column_name: str,
        max_length: int,
        avg_length: int,
        nulls_count: int,
        unique_count: int,
        tags: List[str] = None,
    ) -> None:
        super().__init__(column_name, tags)
        self.max_length = max_length
        self.avg_length = avg_length
        self.nulls_count = nulls_count
        self.unique_count = unique_count

    def to_odd(self, oddrn: str) -> DataSetFieldStat:
        data_entity = super().to_odd(oddrn)
        data_entity.string_stats = StringFieldStat(
            max_length=self.max_length,
            avg_length=round(self.avg_length),
            nulls_count=self.nulls_count,
            unique_count=self.unique_count,
        )

        return data_entity
