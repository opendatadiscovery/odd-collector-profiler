import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Optional

from dataprofiler import Profiler, dp_logging
from funcy import first
from pandas import DataFrame

from odd_collector_profiler.domain.statistics import (ColumnStatistic,
                                                      DatetimeColumnStatistic,
                                                      IntColumnStatistic,
                                                      StringColumnStatistic)
from odd_collector_profiler.utils.datetime import parse_datetime

dp_logging.set_verbosity(logging.ERROR)


class DataProfiler(ABC):
    @staticmethod
    @abstractmethod
    def from_df(df: DataFrame) -> List[ColumnStatistic]:
        """Crates ColumnStatistic from DataFrames"""
        raise NotImplementedError


class DefaultDataProfiler(DataProfiler):
    def from_df(self, df: DataFrame) -> Iterable[ColumnStatistic]:
        stats = []

        for column_stat in (
            Profiler(df)
            .report(report_options={"output_format": "compact"})
            .get("data_stats")
        ):
            stat = self.__get_statistic(column_stat)
            if stat is not None:
                stats.append(stat)

        return stats

    def __get_statistic(self, column_stat: Dict[str, Any]) -> Optional[ColumnStatistic]:
        column_type = column_stat.get("data_type")
        column_name = column_stat.get("column_name")
        statistics = column_stat.get("statistics")

        fns = {
            "int": self.get_int_stat,
            "string": self.get_str_stat,
            "datetime": self.get_datetime_stat,
        }

        if column_type not in fns:
            logging.debug("unknown type")
            logging.debug(column_stat["column_name"], column_stat["data_type"])
            return None

        return fns[column_type](column_name, statistics)

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
            mean_value=None,
            median_value=None,
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
    def get_str_stat(name: str, statistics: Dict[str, Any]) -> StringColumnStatistic:
        return StringColumnStatistic(
            column_name=name,
            max_length=statistics.get("max"),
            avg_length=round(statistics.get("mean")),
            nulls_count=statistics.get("unique_count"),
            unique_count=statistics.get("null_count"),
        )
