import traceback
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd
from sqlalchemy.engine import Connection

from odd_collector_profiler.logger import logger


class DataFrameReader(ABC):
    @abstractmethod
    def read(self, sample_size: Optional[int] = None) -> pd.DataFrame:
        raise NotImplementedError


class TableDataframeReader(DataFrameReader):
    def __init__(
        self, table: str, connection: Connection, schema: Optional[str] = None
    ):
        self.table = table
        self.connection = connection
        self.schema = schema

    def read(self, sample_size: Optional[int] = None) -> pd.DataFrame:
        try:
            return pd.read_sql_table(
                table_name=self.table,
                schema=self.schema,
                con=self.connection,
            ).sample(sample_size)
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(f"Getting data frame, {e}")
