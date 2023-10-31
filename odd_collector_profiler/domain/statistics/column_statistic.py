from abc import ABC
from typing import List

from odd_models.models import DataSetFieldStat, Tag


class ColumnStatistic(ABC):
    def __init__(
        self,
        column_name: str,
        tags: List[str] = None,
    ) -> None:
        self.column_name = column_name
        self.tags = tags or []

    def to_odd(self) -> DataSetFieldStat:
        tags = [Tag(name=name) for name in self.tags]
        return DataSetFieldStat(tags=tags)
