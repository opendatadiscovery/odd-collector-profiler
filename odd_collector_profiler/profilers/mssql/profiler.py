from typing import Any

from oddrn_generator import OdbcGenerator

from odd_collector_profiler.datasource.database.profiler import RDBProfiler
from odd_collector_profiler.datasource.database.repository import RDBRepository
from odd_collector_profiler.domain.config import MSSqlConfig, PostgresConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.profilers import DATA_PROFILER

SYS_SCHEMAS = {
    "db_owner",
    "db_accessadmin",
    "db_securityadmin",
    "db_ddladmin",
    "db_backupoperator",
    "db_datareader",
    "db_datawriter",
    "db_denydatareader",
    "db_denydatawriter",
    "INFORMATION_SCHEMA",
    "sys",
    "guest",
}


class MssqlProfiler(RDBProfiler):
    config_model = PostgresConfig
    """Profiler for Mssql datasource"""


def register_profiler(config: dict[str, Any]) -> Profiler:
    config = MSSqlConfig.parse_obj(config)
    repository = RDBRepository(config=config, skip_schemas=SYS_SCHEMAS)
    generator = OdbcGenerator(host_settings=config.host, databases=config.database)
    return MssqlProfiler(
        config=config,
        generator=generator,
        repository=repository,
        profiler=DATA_PROFILER,
    )
