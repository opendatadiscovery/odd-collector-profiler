from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar

from odd_models.models import DataSetStatistics
from pydantic import ValidationError

from ..errors import InvalidConfigError
from .config import Config

T = TypeVar("T", bound=Config)


class Profiler(ABC):
    """
    Abstract class for datasource profilers
    :param config_model describes config for certain datasource, i.e PostgresConfig
    """

    config_model: Type[T]

    def __init__(self, config: Dict[str, Any]):
        self.config = self._create_config(config)

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
