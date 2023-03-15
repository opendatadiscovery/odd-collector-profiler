import traceback
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd
from sqlalchemy.engine import Connection

from odd_collector_profiler.logger import logger


class DataFrameReader(ABC):
    @abstractmethod
    def read(self) -> pd.DataFrame:
        raise NotImplementedError


class TableDataframeReader(DataFrameReader):
    def __init__(
        self, table: str, connection: Connection, schema: Optional[str] = None
    ):
        self.table = table
        self.connection = connection
        self.schema = schema

    def read(self) -> pd.DataFrame:
        try:
            return pd.read_sql_table(
                table_name=self.table,
                schema=self.schema,
                con=self.connection,
            ).head(
                5000
            )  # make stats by first 5000 rows to save time and capacity. The exact stats are not required
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(f"Getting data frame, {e}")
