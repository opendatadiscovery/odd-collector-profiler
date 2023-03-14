from typing import Any, Dict, List, Tuple

from funcy import lmap
from odd_models.models import DataSetFieldStat, DataSetStatistics, DatasetStatisticsList
from oddrn_generator import AzureSQLGenerator
from sqlalchemy import text
from sqlalchemy.engine import Connection

from odd_collector_profiler.domain.config import AzureSQLConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.domain.statistics.column_statistic import ColumnStatistic
from odd_collector_profiler.helpers.sql_dialect import SQLDialect
from odd_collector_profiler.profilers import DATA_PROFILER
from odd_collector_profiler.services.data_frame_reader import TableDataframeReader
from odd_collector_profiler.services.data_profiler import DataProfiler


class AzureSQLProfiler(Profiler, SQLDialect):
    """Profiler for Postgresql datasource"""

    config_model = AzureSQLConfig
    data_frame_reader = TableDataframeReader

    def __init__(self, config: Dict[str, Any], data_profiler: DataProfiler):
        super().__init__(config, data_profiler)
        self.generator = AzureSQLGenerator(
            host_settings=f"{self.config.server}.database.windows.net:{self.config.port}",
            databases=self.config.database
        )

    def get_statistics(self) -> DatasetStatisticsList:
        items: List[DataSetStatistics] = []

        with self.connect() as connection:
            query = "SELECT name FROM sys.schemas WHERE principal_id=1"
            query_result = connection.execute(text(query))
            main_schemas = [i[0] for i in query_result.fetchall()]
            for schema in main_schemas:
                items.extend(
                    self.get_dataset_statistic(schema, table, connection)
                    for table in self.get_tables(schema)
                )

            return DatasetStatisticsList(items=items)

    def get_dataset_statistic(
        self, schema: str, table: str, connection: Connection
    ) -> DataSetStatistics:

        reader = TableDataframeReader(table=table, schema=schema, connection=connection)

        self.generator.set_oddrn_paths(schemas=schema, tables=table)

        fields = lmap(
            self.map_column_stat, self.data_profiler.from_data_frame(reader.read())
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
    return AzureSQLProfiler(config=config, data_profiler=DATA_PROFILER)
