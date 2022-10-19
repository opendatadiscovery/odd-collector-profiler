from datetime import datetime
from typing import Callable

import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class TaskRunner:
    """
    :property interval - polling interval in minutes
    :property func - function to execute
    """

    def __init__(self, func: Callable, interval: int):
        self.__func = func
        self.__interval = interval

    def start(self):
        scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        scheduler.add_job(
            self.__func,
            "interval",
            minutes=self.__interval,
            next_run_time=datetime.now(),
        )
        scheduler.start()
