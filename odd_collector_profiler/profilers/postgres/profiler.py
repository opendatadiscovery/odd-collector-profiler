from typing import Any

from oddrn_generator import PostgresqlGenerator

from odd_collector_profiler.datasource.database.profiler import RDBProfiler
from odd_collector_profiler.datasource.database.repository import RDBRepository
from odd_collector_profiler.domain.config import PostgresConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.profilers import DATA_PROFILER

SYS_SCHEMAS = {"information_schema", "pg_catalog"}


class PostgresProfiler(RDBProfiler):
    config_model = PostgresConfig
    """Profiler for Postgresql datasource"""


def register_profiler(config: dict[str, Any]) -> Profiler:
    config = PostgresConfig.parse_obj(config)
    repository = RDBRepository(config=config, skip_schemas=SYS_SCHEMAS)
    generator = PostgresqlGenerator(
        host_settings=config.host, databases=config.database
    )
    return PostgresProfiler(
        config=config,
        generator=generator,
        repository=repository,
        profiler=DATA_PROFILER,
    )
