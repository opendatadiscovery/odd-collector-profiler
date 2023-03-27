from typing import Any

from oddrn_generator import AzureSQLGenerator

from odd_collector_profiler.datasource.database.profiler import RDBProfiler
from odd_collector_profiler.datasource.database.repository import AzureSLQRepository
from odd_collector_profiler.domain.config import AzureSQLConfig
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


class AzureProfiler(RDBProfiler):
    config_model = AzureSQLConfig
    """Profiler for AzureSql datasource"""


def register_profiler(config: dict[str, Any]) -> Profiler:
    config = AzureSQLConfig.parse_obj(config)
    repository = AzureSLQRepository(config=config, skip_schemas=SYS_SCHEMAS)
    generator = AzureSQLGenerator(
        host_settings=f"{config.host}:{config.port}", databases=config.database
    )

    return AzureProfiler(
        config=config,
        generator=generator,
        repository=repository,
        profiler=DATA_PROFILER,
    )
