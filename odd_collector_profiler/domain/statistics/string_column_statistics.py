from dataclasses import dataclass

from odd_models.models import DataSetFieldStat, StringFieldStat

from .column_statistic import ColumnStatistic


@dataclass
class StringColumnStatistic(ColumnStatistic):
    max_length: int
    avg_length: int
    nulls_count: int
    unique_count: int

    def to_odd(self, oddrn: str) -> DataSetFieldStat:
        return DataSetFieldStat(
            tags=[],
            field_oddrn=oddrn,
            string_stats=StringFieldStat(
                max_length=self.max_length,
                avg_length=round(self.avg_length),
                nulls_count=self.nulls_count,
                unique_count=self.unique_count,
            ),
        )
