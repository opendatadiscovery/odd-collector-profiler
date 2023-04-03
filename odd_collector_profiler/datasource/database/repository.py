from contextlib import contextmanager

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Connection, Engine, Inspector

from odd_collector_profiler.datasource.database.table import Table
from odd_collector_profiler.domain.config import DatabaseConfig
from odd_collector_profiler.logger import logger


class Repository:
    skip_schemas = set()

    @property
    def engine(self) -> Engine:
        return create_engine(self.config.connection_str())

    @property
    def inspector(self) -> Inspector:
        return inspect(self.engine)

    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config

    def _get_schemas(self):
        yield from self.inspector.get_schema_names()

    def _get_tables_by(self, schema: str = None):
        yield from self.inspector.get_table_names(schema=schema)

    def get_tables(self) -> list[Table]:
        for schema in self._get_schemas():
            logger.debug(f"schema: {schema}")
            for table in self._get_tables_by(schema):
                logger.debug(f"{schema=} {table=}")
                yield Table(database=self.config.database, schema=schema, name=table)

    @contextmanager
    def connect(self) -> Connection:
        with self.engine.connect() as connection:
            yield connection


class RDBRepository(Repository):
    def __init__(self, config: DatabaseConfig, skip_schemas: set[str] = None) -> None:
        super().__init__(config)
        self.skip_schemas = skip_schemas or set()

    def _get_schemas(self):
        for schema in super()._get_schemas():
            if schema not in self.skip_schemas:
                yield schema

    def get_tables(self) -> list[Table]:
        if not self.config.filters:
            yield from super().get_tables()
        else:
            logger.debug(f"filters: {self.config.filters}")
            for schema, tables in self.config.filters.items():
                for table in tables:
                    yield Table(
                        database=self.config.database, schema=schema, name=table
                    )


class MySQLRepository(RDBRepository):
    skip_schemas = {"information_schema", "mysql", "performance_schema", "sys"}

    def get_tables(self) -> list[Table]:
        for table_name in self._get_tables_by(self.config.database):
            if not self.config.filters or table_name in self.config.filters:
                yield Table(database=self.config.database, schema=None, name=table_name)


class AzureSLQRepository(RDBRepository):
    skip_schemas = set()


class ClickHouseRepository(RDBRepository):
    skip_schemas = set()

    def get_tables(self) -> list[Table]:
        for table_name in self._get_tables_by(self.config.database):
            if not self.config.filters or table_name in self.config.filters:
                yield Table(database=self.config.database, schema=None, name=table_name)
