from typing import Any

from oddrn_generator import ClickHouseGenerator

from odd_collector_profiler.datasource.database.profiler import RDBProfiler
from odd_collector_profiler.datasource.database.repository import RDBRepository
from odd_collector_profiler.domain.config import ClickHouseConfig
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.profilers import DATA_PROFILER


class ClickHouseProfiler(RDBProfiler):
    config_model = ClickHouseConfig
    """Profiler for the Clickhouse datasource."""


def register_profiler(config: dict[str, Any]) -> Profiler:
    config = ClickHouseConfig.parse_obj(config)
    repository = RDBRepository(config=config)
    generator = ClickHouseGenerator(
        host_settings=config.host, databases=config.database
    )
    return ClickHouseProfiler(
        config=config,
        generator=generator,
        repository=repository,
        profiler=DATA_PROFILER,
    )
