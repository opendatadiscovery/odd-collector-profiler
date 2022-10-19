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


class S3Config(Config):
    type = "s3"
