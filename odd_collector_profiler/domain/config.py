from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel, SecretStr


class Config(BaseModel):
    type: str
    name: str


class DatabaseConfig(ABC, Config):
    tables: Optional[List[str]] = None

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


class MSSqlConfig(DatabaseConfig):
    type = "mssql"
    scheme: Optional[str] = "mssql+pyodbc"
    host: str
    port: int
    username: str
    password: Optional[SecretStr] = SecretStr("")
    database: str
    driver: str

    def connection_str(self) -> str:
        return (
            f"{self.scheme}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"
            + f"?driver={self.driver}"
        )


class MySqlConfig(DatabaseConfig):
    type = "mysql"
    scheme: Optional[str] = "mysql+pymysql"
    host: str
    port: int
    username: str
    password: Optional[SecretStr] = SecretStr("")
    database: str
    sample_size: Optional[int] = None

    def connection_str(self) -> str:
        return f"{self.scheme}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class S3Config(Config):
    type = "s3"
