import asyncio
import logging
import os

from odd_collector_profiler.profiler_sdk import ProfilerSDK

logging.basicConfig(
    level=os.getenv("LOGLEVEL", "DEBUG"),
    format="[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
)
logger = logging.getLogger("odd-collector-collector")

try:
    loop = asyncio.get_event_loop()

    ProfilerSDK("./collector_config.yaml").start_polling()

    loop.run_forever()
except Exception as exc:
    logging.exception(exc)
    asyncio.get_event_loop().stop()
