import asyncio
import importlib
import signal
import traceback
from functools import partial
from pathlib import Path
from typing import Any, Dict, Optional

from funcy import cached_property
from odd_collector_sdk.api.datasource_api import PlatformApi
from odd_collector_sdk.api.http_client import HttpClient
from odd_collector_sdk.shutdown import shutdown_by
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
    def __init__(self, config_path: Path) -> None:
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
        send_request = partial(self.__send_request)
        tasks = [
            asyncio.create_task(send_request(profiler=profiler))
            for profiler in self.profilers
        ]
        await handle_tasks(tasks)

    async def __send_request(self, profiler: Profiler):
        logger.debug(f"[{profiler.config.name}] Start calculating statistics")
        try:
            dsl = await self.__get_statistics(profiler)
            res = await self.__request(dsl)
            logger.success(f"[{profiler.config.name}] Metadata ingested")
            return res
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(e)

    async def __get_statistics(self, profiler: Profiler):
        result = profiler.get_statistics()
        return await result if asyncio.iscoroutine(result) else result

    async def __request(self, statistics: DatasetStatisticsList):
        res = await self.client.post(
            f"{self.config.platform_host_url}/ingestion/entities/datasets/stats",
            statistics.json(),
        )
        res.raise_for_status()
        return res

    def run(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        try:
            if not loop:
                loop = asyncio.get_event_loop()

            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
            for s in signals:
                loop.add_signal_handler(
                    s, lambda s=s: asyncio.create_task(shutdown_by(s, loop))
                )

            if (
                self.config.default_pulling_interval is None
                or self.config.default_pulling_interval <= 0
            ):
                loop.run_until_complete(self.__ingest_stats())
            else:
                self.start_polling()
                loop.run_forever()
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(e)
