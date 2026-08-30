# src/storage_base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class StorageBase(ABC):
    @abstractmethod
    def add_aircraft(self, aircraft: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_aircraft(self, call_sign: str) -> bool:
        pass

    @abstractmethod
    def filter_by_country(self, country: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
