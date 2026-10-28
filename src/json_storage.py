# src/json_storage.py
import json
from pathlib import Path
from typing import List, Dict, Any

from .storage_base import StorageBase


class JSONStorage(StorageBase):
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.filepath.write_text("[]", encoding="utf-8")

    def _read_data(self) -> List[Dict[str, Any]]:
        try:
            text = self.filepath.read_text(encoding="utf-8")
            data = json.loads(text)
            if not isinstance(data, list):
                return []
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[Dict[str, Any]]) -> None:
        self.filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_aircraft(self, aircraft: Dict[str, Any]) -> None:
        data = self._read_data()
        data.append(aircraft)
        self._write_data(data)

    def get_all(self) -> List[Dict[str, Any]]:
        return self._read_data()

    def delete_aircraft(self, call_sign: str) -> bool:
        data = self._read_data()
        initial_len = len(data)
        data = [a for a in data if a.get("call_sign") != call_sign]
        if len(data) < initial_len:
            self._write_data(data)
            return True
        return False

    def filter_by_country(self, country: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            a
            for a in data
            if a.get("country", "").lower() == country.lower()
        ]

    def clear(self) -> None:
        self._write_data([])
