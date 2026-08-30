# tests/test_main_logic.py
import pytest
from src.main import get_top_n_by_altitude

@pytest.fixture
def mock_bbox():
    return {"south": 0.0, "north": 10.0, "west": 0.0, "east": 10.0}

def test_get_top_n_skips_invalid_altitudes(mock_bbox, monkeypatch):
    mock_states = [
        {
            "icao24": "A1B2C3",
            "name": "Flight1",
            "country": "USA",
            "baro_altitude": 10000.0,
            "velocity": 200.0
        },
        {
            "icao24": "BAD123",
            "name": "",
            "country": "Unknown",
            "baro_altitude": -500.0,  # Отрицательная → ValueError
            "velocity": None
        },
        {
            "icao24": "NULL123",
            "name": "",
            "country": "Canada",
            "baro_altitude": None,     # Превратится в 0 → отфильтруем по условию altitude_m > 0
            "velocity": None
        }
    ]

    def mock_get(*args, **kwargs):
        return mock_states

    from src.opensky_api import OpenSkyAPI
    monkeypatch.setattr(OpenSkyAPI, "get_aircrafts_in_bbox", mock_get)

    result = get_top_n_by_altitude(5, mock_bbox)

    assert len(result) == 1
    assert result[0].call_sign == "A1B2C3"
