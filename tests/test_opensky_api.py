# tests/test_opensky_api.py
import pytest
import responses
from src.opensky_api import OpenSkyAPI

@responses.activate
def test_opensky_get_aircrafts_in_bbox_returns_list():
    mock_states = [
        # [icao24, name, country, ...]
        ["a1b2c3", "Flight1", "USA", 1700000000, None, -90.0, 30.0,
         10000.0, False, 200.0, 90.0, 0.0, None, 10100.0, "7700", False, 0],
        ["d4e5f6", "Flight2", "Canada", 1700000001, None, -80.0, 40.0,
         8000.0, False, 220.0, 120.0, 0.0, None, 8100.0, "1200", False, 0]
    ]
    mock_response = {"states": mock_states}

    responses.add(
        responses.GET,
        "https://opensky-network.org/api/states/all",
        json=mock_response,
        status=200
    )

    api = OpenSkyAPI()
    bbox = {"south": 25.0, "north": 45.0, "west": -100.0, "east": -70.0}
    aircrafts = api.get_aircrafts_in_bbox(bbox)

    assert isinstance(aircrafts, list)
    assert len(aircrafts) == 2
    # Теперь это словари, можно брать по ключу
    assert aircrafts[0]["country"] == "USA"
    assert aircrafts[1]["country"] == "Canada"

@responses.activate
def test_opensky_returns_empty_list_on_no_data():
    responses.add(
        responses.GET,
        "https://opensky-network.org/api/states/all",
        json={"states": []},
        status=200
    )

    api = OpenSkyAPI()
    bbox = {"south": 0.0, "north": 1.0, "west": 0.0, "east": 1.0}
    aircrafts = api.get_aircrafts_in_bbox(bbox)

    assert aircrafts == []
