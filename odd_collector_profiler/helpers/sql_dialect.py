from collections import defaultdict
from contextlib import contextmanager
from typing import Dict, Iterable, List, Set

import pandas as pd
from sqlalchemy import create_engine, inspect, text
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

    def get_base_table_info(self) -> Dict[str, List[str]]:
        """
        Get main schemas and tables as dict:
        {schema_name: [table_name,...,]}
        """
        if self.config.filters:
            return self.config.filters

        # Query to get all information about base table.
        query = """
            SELECT
                table_schema,
                table_name
            FROM information_schema.tables
            WHERE TABLE_TYPE = 'BASE TABLE'
        """
        with self.connect() as connection:
            result_as_dict = defaultdict(list)
            query_result = connection.execute(text(query))
            tuple_with_schema_table = query_result.fetchall()

            for schema, table in tuple_with_schema_table:
                result_as_dict[schema].append(table)

            return result_as_dict

    @staticmethod
    def get_data_frame(table_name: str, connection: Connection):
        return pd.read_sql(table_name, connection)

    @contextmanager
    def connect(self) -> Connection:
        with self.engine.connect() as connection:
            yield connection
