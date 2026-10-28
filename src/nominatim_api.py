# src/nominatim_api.py
import requests
from typing import Any, Dict, List
from .api_base import BaseAPI

NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "AircraftTracker/1.0 (github.com/prudnikovsemen-beep/feature-homework_10_1)"


class NominatimAPI(BaseAPI):
    def get(self, url: str, params: Dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def post(self, url: str, data: Dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        raise NotImplementedError("Nominatim API uses GET only")

    def get_country_bbox(self, country: str) -> Dict[str, float]:
        params = {
            "q": country,
            "format": "json",
            "limit": 1,
        }
        raw_data = self.get(NOMINATIM_SEARCH_URL, params=params)

        # Явная проверка типа: Nominatim всегда возвращает список
        if not isinstance(raw_data, list):
            raise ValueError(f"Unexpected response format for country {country}")

        data: List[Dict[str, Any]] = raw_data

        if not data:
            raise ValueError(f"Country not found: {country}")

        result = data[0]
        bbox_raw = result.get("boundingbox")
        if not bbox_raw:
            raise ValueError(f"No bounding box for country: {country}")

        south, north, west, east = map(float, bbox_raw)
        return {
            "south": south,
            "north": north,
            "west": west,
            "east": east,
        }
