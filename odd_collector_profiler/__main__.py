import asyncio
import logging
import os
from pathlib import Path

from odd_collector_profiler.logger import logger
from odd_collector_profiler.profiler_sdk import ProfilerSDK

try:
    loop = asyncio.get_event_loop()

    ProfilerSDK(Path().cwd() / "collector_config.yaml").start_polling()

    loop.run_forever()
except Exception as exc:
    logger.debug(exc)
    logger.exception(exc)
    asyncio.get_event_loop().stop()
