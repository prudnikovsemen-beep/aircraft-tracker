# tests/test_json_storage.py
import json
from pathlib import Path
from src.json_storage import JSONStorage

def test_add_and_get(tmp_path):
    file_path = tmp_path / "test.json"
    storage = JSONStorage(str(file_path))

    storage.add_aircraft({"call_sign": "TEST1", "country": "USA", "speed_kph": 500, "altitude_m": 1000})
    storage.add_aircraft({"call_sign": "TEST2", "country": "Canada", "speed_kph": 600, "altitude_m": 800})

    data = storage.get_all()
    assert len(data) == 2
    assert data[0]["call_sign"] == "TEST1"
    assert data[1]["call_sign"] == "TEST2"

def test_delete_aircraft(tmp_path):
    file_path = tmp_path / "test.json"
    storage = JSONStorage(str(file_path))

    storage.add_aircraft({"call_sign": "TEST1", "country": "USA", "speed_kph": 500, "altitude_m": 1000})
    deleted = storage.delete_aircraft("TEST1")
    assert deleted is True

    data = storage.get_all()
    assert len(data) == 0

    deleted_again = storage.delete_aircraft("TEST1")
    assert deleted_again is False

def test_filter_by_country(tmp_path):
    file_path = tmp_path / "test.json"
    storage = JSONStorage(str(file_path))

    storage.add_aircraft({"call_sign": "A1", "country": "USA", "speed_kph": 500, "altitude_m": 1000})
    storage.add_aircraft({"call_sign": "A2", "country": "Canada", "speed_kph": 600, "altitude_m": 800})
    storage.add_aircraft({"call_sign": "A3", "country": "usa", "speed_kph": 700, "altitude_m": 900})  # регистронезависимо

    filtered = storage.filter_by_country("USA")
    assert len(filtered) == 2
    calls = [a["call_sign"] for a in filtered]
    assert "A1" in calls and "A3" in calls
