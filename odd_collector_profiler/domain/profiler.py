from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar

from odd_models.models import DataSetStatistics
from pydantic import ValidationError

from odd_collector_profiler.services.data_profiler import DataProfiler

from ..errors import InvalidConfigError
from .config import Config

T = TypeVar("T", bound=Config)


class Profiler(ABC):
    """
    Abstract class for datasource profilers
    :param config_model describes config for certain datasource, i.e PostgresConfig
    :param data_profiler is 3rd part library generates reports
    """

    config_model: Type[T]
    data_profiler: DataProfiler = None

    def __init__(self, config: Dict[str, Any], data_profiler: DataProfiler):
        self.config = self._create_config(config)
        self.data_profiler = data_profiler

    def _create_config(self, config: Dict[str, Any]) -> T:
        try:
            return self.config_model.parse_obj(config)
        except ValidationError as err:
            raise InvalidConfigError from err

    @property
    def name(self) -> str:
        return self.config.name

    @abstractmethod
    def get_statistics(self) -> DataSetStatistics:
        raise NotImplementedError
