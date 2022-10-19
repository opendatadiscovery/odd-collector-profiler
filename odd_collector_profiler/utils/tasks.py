import logging
from asyncio import FIRST_EXCEPTION, Task, wait
from typing import List


async def handle_tasks(tasks: List[Task]):
    """
    Wait taks, on the exception log it and run next tasks
    """

    finished, not_finished = await wait(tasks, return_when=FIRST_EXCEPTION)

    for task in finished:
        if task.exception():
            logging.error("Error during run task", exc_info=task.exception())
            await handle_tasks(not_finished)
