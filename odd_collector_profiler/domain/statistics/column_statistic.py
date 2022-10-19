from abc import ABC
from dataclasses import dataclass

from odd_models.models import DataSetFieldStat


@dataclass
class ColumnStatistic(ABC):
    column_name: str

    def to_odd(self, oddrn: str) -> DataSetFieldStat:
        raise NotImplementedError
