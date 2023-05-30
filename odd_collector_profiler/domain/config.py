from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List, Optional

from pydantic import BaseModel, SecretStr
from sqlalchemy.engine import URL


class Config(BaseModel):
    type: str
    name: str


class DatabaseConfig(ABC, Config):
    tables: Optional[List[str]] = None
    filters: Optional[dict[str, list[str]]] = None

    @abstractmethod
    def connection_str(self) -> str:
        raise NotImplementedError


class PostgresConfig(DatabaseConfig):
    type = "postgres"
    scheme: Optional[str] = "postgresql"
    host: str
    port: int
    username: str
    password: Optional[SecretStr] = SecretStr("")
    database: str

    def connection_str(self) -> str:
        return f"{self.scheme}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class S3Config(Config):
    type = "s3"


class MySqlConfig(DatabaseConfig):
    type = "mysql"
    scheme: Optional[str] = "mysql+pymysql"
    host: str
    port: int
    username: str
    password: Optional[SecretStr] = SecretStr("")
    database: str
    filters: Optional[list[str]] = None

    def connection_str(self) -> str:
        return f"{self.scheme}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class MSSqlConfig(DatabaseConfig):
    type = "mssql"
    database: str
    host: str
    port: str
    username: str
    password: str
    encrypt: str = "no"
    trust_server_certificate: str = "yes"
    connection_timeout = 30

    def connection_str(self) -> str:
        connection_string = dedent(
            """
            Driver={driver};
            Server={host};
            Database={database};
            Uid={username};
            Pwd={password};
            Encrypt={encrypt};
            TrustServerCertificate={trust_server_certificate};
            Connection Timeout={connection_timeout};
            """.format(
                driver="{ODBC Driver 18 for SQL Server}",
                database=self.database,
                host="{server_name},{port}".format(
                    server_name=self.host, port=self.port
                ),
                username=self.username,
                password=self.password,
                encrypt=self.encrypt,
                trust_server_certificate=self.trust_server_certificate,
                connection_timeout=self.connection_timeout,
            )
        )
        return URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})


class AzureSQLConfig(MSSqlConfig):
    type = "azure_sql"


class ClickHouseConfig(DatabaseConfig):
    type = "clickhouse"
    database: str
    host: str
    port: str
    username: str
    password: Optional[SecretStr] = SecretStr("")

    def connection_str(self) -> str:
        conn_str = f"clickhouse://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        return conn_str


class OracleConfig(DatabaseConfig):
    type = "oracle"
    host: str
    port: str
    user: str
    database: str
    password: SecretStr
    thick_mode: Optional[bool] = False

    def connection_str(self) -> str:
        conn_str = f"oracle+cx_oracle://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}" \
                   f"/?service_name={self.database}"
        return conn_str
