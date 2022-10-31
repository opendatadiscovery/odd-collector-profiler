import logging
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd
from sqlalchemy.engine import Connection


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
            df = pd.read_sql_table(
                table_name=self.table,
                schema=self.schema,
                con=self.connection,
            )
            return df
        except Exception as e:
            logging.error(f"Getting data frame, {e}", exc_info=True)
