from typing import Any, Dict, List, Optional, Tuple

from funcy import lmap
from odd_models.models import (
    DataEntity,
    DataEntityGroup,
    DataEntityType,
    DataSet,
    DataSetFieldStat,
    DataSetStatistics,
    DatasetStatisticsList,
)
from oddrn_generator import MysqlGenerator
from sqlalchemy.engine import Connection

from odd_collector_profiler.domain.config import MySqlConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.domain.statistics.column_statistic import ColumnStatistic
from odd_collector_profiler.helpers.sql_dialect import SQLDialect
from odd_collector_profiler.profilers import DATA_PROFILER
from odd_collector_profiler.services.data_frame_reader import TableDataframeReader
from odd_collector_profiler.services.data_profiler import DataProfiler


class MySqlProfiler(Profiler, SQLDialect):
    """Profiler for MySql datasource"""

    skip_schemas: set[str] = {"performance_schema", "sys", "mysql"}

    config_model = MySqlConfig
    data_frame_reader = TableDataframeReader

    def __init__(self, config: Dict[str, Any], data_profiler: DataProfiler):
        super().__init__(config, data_profiler)
        self.generator = MysqlGenerator(
            host_settings=self.config.host, databases=self.config.database
        )
        self.sample_size = self.config.sample_size

    def get_statistics(self) -> DatasetStatisticsList:
        items: List[DataSetStatistics] = []

        with self.connect() as connection:
            items.extend(
                self.get_dataset_statistic(table, connection, self.sample_size)
                for table in self.get_tables()
            )

            return DatasetStatisticsList(items=items)

    def get_dataset_statistic(
        self, table: str, connection: Connection, sample_size: Optional[int]
    ) -> DataSetStatistics:
        reader = TableDataframeReader(table=table, connection=connection)

        self.generator.set_oddrn_paths(tables=table)

        fields = lmap(
            self.map_column_stat,
            self.data_profiler.from_data_frame(reader.read(sample_size=sample_size)),
        )

        return DataSetStatistics(
            dataset_oddrn=self.generator.get_oddrn_by_path("tables"),
            fields=dict(fields),
        )

    def map_column_stat(
        self, column_stat: ColumnStatistic
    ) -> Tuple[str, DataSetFieldStat]:
        oddrn = self.generator.get_oddrn_by_path(
            "tables_columns", new_value=column_stat.column_name
        )
        return oddrn, column_stat.to_odd(oddrn=oddrn)


def register_profiler(config: Dict[str, Any]) -> Profiler:
    return MySqlProfiler(config=config, data_profiler=DATA_PROFILER)
