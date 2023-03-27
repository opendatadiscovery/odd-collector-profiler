import asyncio
from pathlib import Path

from odd_collector_profiler.profiler_sdk import ProfilerSDK

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    sdk = ProfilerSDK(Path().cwd() / "collector_config.yaml")
    sdk.run(loop=loop)
