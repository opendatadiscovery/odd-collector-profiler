import traceback
from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd
from sqlalchemy.engine import Connection

from odd_collector_profiler.logger import logger


class DataFrameReader(ABC):
    @abstractmethod
    def read(self, sample_size: Optional[int] = None) -> pd.DataFrame:
        raise NotImplementedError


class TableDataframeReader(DataFrameReader):
    def __init__(self, table: Any, connection: Connection):
        self.table = table
        self.connection = connection

    def read(self) -> pd.DataFrame:
        try:
            return pd.read_sql_table(
                table_name=self.table.name,
                schema=self.table.schema,
                con=self.connection,
            )
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(f"Getting data frame, {e}")


def read_table(table: Any, connection: Connection) -> pd.DataFrame:
    try:
        return pd.read_sql_table(
            table_name=table.name,
            schema=table.schema,
            con=connection,
        )
    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.error(f"Getting data frame, {e}")
