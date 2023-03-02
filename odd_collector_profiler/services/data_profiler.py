import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional

from dataprofiler import Profiler, dp_logging
from funcy import first, lkeep
from pandas import DataFrame

from odd_collector_profiler.domain.statistics import (
    ColumnStatistic,
    DatetimeColumnStatistic,
    IntColumnStatistic,
    NumberColumnStatistic,
    StringColumnStatistic,
)
from odd_collector_profiler.logger import logger
from odd_collector_profiler.utils.datetime import parse_datetime

dp_logging.set_verbosity(logging.ERROR)
SKIP_LABELS = {"UNKNOWN"}


class DataProfiler(ABC):
    @staticmethod
    @abstractmethod
    def from_data_frame(df: DataFrame) -> List[ColumnStatistic]:
        """Crates ColumnStatistic from DataFrames"""
        raise NotImplementedError


class DefaultDataProfiler(DataProfiler):
    def from_data_frame(self, df: DataFrame) -> Iterable[ColumnStatistic]:
        columns_statistics = (
            Profiler(data=df, profiler_type="structured").report().get("data_stats")
        )
        return lkeep(self.__map_statistic, columns_statistics)

    def __map_statistic(self, column_stat: Dict[str, Any]) -> Optional[ColumnStatistic]:
        column_type = column_stat.get("data_type")
        column_name = column_stat.get("column_name")
        statistics = column_stat.get("statistics")
        label = column_stat.get("data_label")

        get_statistics_for: Dict[str, Callable[..., Optional[ColumnStatistic]]] = {
            "int": self.get_int_stat,
            "string": self.get_str_stat,
            "datetime": self.get_datetime_stat,
            "float": self.get_number_stat,
        }

        if column_type not in get_statistics_for:
            logger.debug(f"Unknown type for {column_name} with type {column_type}")
            return None

        column_statistics = get_statistics_for[column_type](column_name, statistics)

        if label:
            tags = [label for label in label.split("|") if label not in SKIP_LABELS]
            column_statistics.tags = tags

        return column_statistics

    @staticmethod
    def get_datetime_stat(
        name: str, statistics: Dict[str, Any]
    ) -> DatetimeColumnStatistic:
        date_format = first(
            statistics.get("format")
        )  # Formats is a list of datetime formats, took first

        return DatetimeColumnStatistic(
            column_name=name,
            low_value=parse_datetime(statistics.get("min"), date_format),
            high_value=parse_datetime(statistics.get("max"), date_format),
            nulls_count=statistics.get("null_count"),
            unique_count=statistics.get("unique_count"),
        )

    @staticmethod
    def get_int_stat(name: str, statistics: Dict[str, Any]) -> IntColumnStatistic:
        return IntColumnStatistic(
            column_name=name,
            low_value=statistics.get("min"),
            high_value=statistics.get("max"),
            mean_value=statistics.get("mean"),
            median_value=statistics.get("median"),
            nulls_count=statistics.get("null_count"),
            unique_count=statistics.get("unique_count"),
        )

    @staticmethod
    def get_number_stat(name: str, statistics: Dict[str, Any]) -> NumberColumnStatistic:
        return NumberColumnStatistic(
            column_name=name,
            low_value=statistics.get("min"),
            high_value=statistics.get("max"),
            mean_value=statistics.get("mean"),
            median_value=statistics.get("median"),
            nulls_count=statistics.get("null_count"),
            unique_count=statistics.get("unique_count"),
        )

    @staticmethod
    def get_str_stat(name: str, statistics: Dict[str, Any]) -> StringColumnStatistic:
        return StringColumnStatistic(
            column_name=name,
            max_length=statistics.get("max"),
            avg_length=round(statistics.get("mean")),
            nulls_count=statistics.get("null_count"),
            unique_count=statistics.get("unique_count"),
        )
