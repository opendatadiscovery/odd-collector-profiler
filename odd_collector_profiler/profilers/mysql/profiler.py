from typing import Any

from oddrn_generator import MysqlGenerator

from odd_collector_profiler.datasource.database.profiler import RDBProfiler
from odd_collector_profiler.datasource.database.repository import MySQLRepository
from odd_collector_profiler.datasource.database.table import Table
from odd_collector_profiler.domain.config import MySqlConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.profilers import DATA_PROFILER


class MySqlProfiler(RDBProfiler):
    config_model = MySqlConfig
    """Profiler for Postgresql datasource"""

    def get_table_oddrn(self, table: Table) -> str:
        self.generator.set_oddrn_paths(tables=table.name)
        return self.generator.get_oddrn_by_path("tables")


def register_profiler(config: dict[str, Any]) -> Profiler:
    config = MySqlConfig.parse_obj(config)
    repository = MySQLRepository(
        config=config,
        skip_schemas={"information_schema", "mysql", "performance_schema", "sys"},
    )
    generator = MysqlGenerator(host_settings=config.host, databases=config.database)
    return MySqlProfiler(
        config=config,
        generator=generator,
        repository=repository,
        profiler=DATA_PROFILER,
    )
