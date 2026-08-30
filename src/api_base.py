# src/api_base.py
from abc import ABC, abstractmethod
from typing import Any


class BaseAPI(ABC):
    @abstractmethod
    def get(self, url: str, params: dict[str, Any] | None = None) -> list[Any] | dict[str, Any]:
        pass

    @abstractmethod
    def post(self, url: str, data: dict[str, Any] | None = None) -> list[Any] | dict[str, Any]:
        pass
