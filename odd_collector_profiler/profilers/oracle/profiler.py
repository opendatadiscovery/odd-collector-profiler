from typing import Any

from oddrn_generator import OracleGenerator

from odd_collector_profiler.datasource.database.profiler import RDBProfiler
from odd_collector_profiler.datasource.database.repository import OracleRepository
from odd_collector_profiler.domain.config import OracleConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.profilers import DATA_PROFILER

SYS_SCHEMAS = {
    "xdb",
    "xs$null",
    "anonymous",
    "apex_040000",
    "apex_public_user",
    "ctxsys",
    "flows_files",
    "hr",
    "mdsys",
    "outln",
    "sys",
    "system",
}


class OracleProfiler(RDBProfiler):
    config_model = OracleConfig
    """Profiler for Oracle datasource"""


def register_profiler(config: dict[str, Any]) -> Profiler:
    config = OracleConfig.parse_obj(config)
    repository = OracleRepository(config=config, skip_schemas=SYS_SCHEMAS)
    generator = OracleGenerator(
        host_settings=config.host, databases=config.database, schemas=config.user
    )
    return OracleProfiler(
        config=config,
        generator=generator,
        repository=repository,
        profiler=DATA_PROFILER,
    )
