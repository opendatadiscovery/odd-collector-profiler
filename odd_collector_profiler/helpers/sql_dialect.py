from contextlib import contextmanager
from typing import Iterable, Set

import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Connection, Engine, Inspector

from odd_collector_profiler.domain.config import DatabaseConfig


def get_data_frame(table_name: str, connection: Connection):
    return pd.read_sql(table_name, connection)


class SQLDialect:
    config: DatabaseConfig
    skip_schemas: Set[str] = {"information_schema"}

    @property
    def engine(self) -> Engine:
        return create_engine(self.config.connection_str())

    @property
    def inspector(self) -> Inspector:
        return inspect(self.engine)

    def get_schemas(self):
        for schema_name in self.inspector.get_schema_names():
            if schema_name not in self.skip_schemas:
                yield schema_name

    def get_tables(self, schema: str = None) -> Iterable[str]:
        tables = self.config.tables or self.inspector.get_table_names(schema)

        for table_name in tables:
            yield table_name

    @staticmethod
    def get_data_frame(table_name: str, connection: Connection):
        return pd.read_sql(table_name, connection)

    @contextmanager
    def connect(self) -> Connection:
        with self.engine.connect() as connection:
            yield connection
