# src/opensky_api.py
import requests
from typing import Any, Dict, List
from .api_base import BaseAPI

OPENSKY_STATES_URL = "https://opensky-network.org/api/states/all"
USER_AGENT = "AircraftTracker/1.0 (github.com/prudnikovsemen-beep/feature-homework_10_1)"


class OpenSkyAPI(BaseAPI):
    def get(self, url: str, params: Dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def post(self, url: str, data: Dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        raise NotImplementedError("OpenSky API uses GET only")

    @staticmethod
    def _parse_state_row(row: list[Any]) -> Dict[str, Any]:
        if not row:
            return {}
        return {
            "icao24": row[0] or "UNKNOWN",
            "name": row[1] or "",
            "country": row[2] or "Unknown",
            "time_position": row[3],
            "last_position": row[4],
            "longitude": row[5],
            "latitude": row[6],
            "baro_altitude": row[7],
            "on_ground": row[8],
            "velocity": row[9],
            "true_track": row[10],
            "vertical_rate": row[11],
            "sensors": row[12],
            "geo_altitude": row[13],
            "squawk": row[14],
            "spi": row[15],
            "position_source": row[16],
        }

    def get_aircrafts_in_bbox(
        self, bbox: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        params = {
            "lamin": bbox["south"],
            "lamax": bbox["north"],
            "lomin": bbox["west"],
            "lomax": bbox["east"],
        }
        data = self.get(OPENSKY_STATES_URL, params=params)
        # OpenSky реально возвращает dict с ключом states
        if not isinstance(data, dict):
            raise RuntimeError("Unexpected response format from OpenSky API")
        states = data.get("states", [])
        return [self._parse_state_row(row) for row in states]
