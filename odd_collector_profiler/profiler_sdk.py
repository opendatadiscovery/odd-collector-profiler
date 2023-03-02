import asyncio
import importlib
import traceback
from functools import partial
from pathlib import Path
from typing import Any, Dict

from aiohttp import ClientSession
from funcy import cached_property
from odd_collector_sdk.api.datasource_api import PlatformApi
from odd_collector_sdk.api.http_client import HttpClient
from odd_models.models import DatasetStatisticsList

from odd_collector_profiler.domain.collector_profiler_config import (
    CollectorProfilerConfig,
)
from odd_collector_profiler.domain.profiler import Profiler
from odd_collector_profiler.errors import MissedRegisterFunction
from odd_collector_profiler.helpers.task_runner import TaskRunner
from odd_collector_profiler.logger import logger
from odd_collector_profiler.utils.tasks import handle_tasks


def register_profiler(cfg: Dict[str, Any]):
    module_type = importlib.import_module(
        f"odd_collector_profiler.profilers.{cfg['type']}.profiler"
    )

    try:
        return module_type.register_profiler(cfg)
    except AttributeError as err:
        raise MissedRegisterFunction(cfg["type"]) from err


class ProfilerSDK:
    def __init__(self, config_path: Path):
        self.config = CollectorProfilerConfig.from_yaml(str(config_path))
        self.client = HttpClient(self.config.token)
        self.api = PlatformApi(self.client, self.config.platform_host_url)
        self.task_runner = TaskRunner(
            self.__ingest_stats, self.config.default_pulling_interval
        )

    @cached_property
    def profilers(self):
        """Import profilers module to collect statistics for them later"""
        return [register_profiler(cfg) for cfg in self.config.profilers]

    def start_polling(self):
        """Start polling profilers"""
        self.task_runner.start()

    async def __ingest_stats(self):
        async with ClientSession() as session:
            send_request = partial(self.__send_request, session=session)
            tasks = [
                asyncio.create_task(send_request(profiler=profiler))
                for profiler in self.profilers
            ]
            res = await handle_tasks(tasks)

    async def __send_request(self, profiler: Profiler, session: ClientSession):
        logger.debug(f"[{profiler.config.name}] Start calculating statistics")
        try:
            dsl = await self.__get_statistics(profiler)
            res = await self.__request(dsl, session)
            logger.success(f"[{profiler.config.name}] Metadata ingested")
            return res
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(e)

    async def __get_statistics(self, profiler: Profiler):
        result = profiler.get_statistics()
        res = await result if asyncio.iscoroutine(result) else result
        return res

    async def __request(
        self, statistics: DatasetStatisticsList, session: ClientSession
    ):
        res = await self.client.post(
            f"{self.config.platform_host_url}/ingestion/entities/datasets/stats",
            statistics.json(),
            session,
        )
        res.raise_for_status()
        return res
