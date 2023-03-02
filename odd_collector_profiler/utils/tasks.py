import traceback
from asyncio import FIRST_EXCEPTION, Task, wait
from typing import List

from odd_collector_profiler.logger import logger


async def handle_tasks(tasks: List[Task]):
    """
    Wait taks, on the exception log it and run next tasks
    """

    finished, not_finished = await wait(tasks, return_when=FIRST_EXCEPTION)

    for task in finished:
        if task.exception():
            logger.debug(traceback.format_exc())
            logger.error("Error during run task")
            await handle_tasks(not_finished)
