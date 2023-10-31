import traceback

import pandas
from odd_models import DataSetStatistics, DatasetStatisticsList
from oddrn_generator import Generator

from odd_collector_profiler.data_frame_reader import read_table
from odd_collector_profiler.data_profiler import DataProfiler
from odd_collector_profiler.datasource.database.repository import Repository
from odd_collector_profiler.datasource.database.table import Table
from odd_collector_profiler.domain.config import DatabaseConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.domain.statistics.column_statistic import ColumnStatistic
from odd_collector_profiler.logger import logger

RDBS_WITHOUT_SCHEMA = ["clickhouse"]


class RDBProfiler(Profiler):
    def __init__(
        self,
        config: DatabaseConfig,
        repository: Repository,
        generator: Generator,
        profiler: DataProfiler,
    ) -> None:
        self.config = config
        self.repo = repository
        self.generator = generator
        self.profiler = profiler

    def get_statistics(self) -> DatasetStatisticsList:
        items: list[DataSetStatistics] = []
        for table in self.repo.get_tables():
            data_frame = self.get_data_frame(table)
            profile = self.profiler.from_data_frame(df=data_frame)

            dataset_oddrn = self.get_table_oddrn(table)

            fields = {}
            for field_stat in profile:
                field_oddrn = self.get_field_oddrn(field_stat)
                fields[field_oddrn] = field_stat.to_odd()
            items.append(DataSetStatistics(dataset_oddrn=dataset_oddrn, fields=fields))

        return DatasetStatisticsList(items=items)

    def get_table_oddrn(self, table: Table) -> str:
        if self.config.type not in RDBS_WITHOUT_SCHEMA:
            self.generator.set_oddrn_paths(schemas=table.schema, tables=table.name)
        else:
            self.generator.set_oddrn_paths(tables=table.name)
        return self.generator.get_oddrn_by_path("tables")

    def get_field_oddrn(self, c: ColumnStatistic) -> str:
        return self.generator.get_oddrn_by_path("tables_columns", c.column_name)

    def get_data_frame(self, table: Table) -> pandas.DataFrame:
        try:
            with self.repo.connect() as conn:
                return read_table(table, conn)
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(f"Getting data frame, {e}")
