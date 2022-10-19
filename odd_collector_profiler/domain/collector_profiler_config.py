from typing import Any, List

from pyaml_env import parse_config
from pydantic import BaseSettings


class CollectorProfilerConfig(BaseSettings):
    default_pulling_interval: int
    token: str
    profilers: List[Any]
    platform_host_url: str

    @classmethod
    def from_yaml(cls, path: str):
        return cls.parse_obj(parse_config(path))
