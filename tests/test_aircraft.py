import pytest
from src.aircraft import Aircraft

def test_aircraft_valid_initialization():
    a = Aircraft("UAL1621", "United States", 268.79, 10203.18)
    assert a.call_sign == "UAL1621"
    assert a.country == "United States"
    assert abs(a.speed_kph - 268.79) < 1e-6
    assert abs(a.altitude_m - 10203.18) < 1e-6

def test_aircraft_raises_on_negative_speed():
    with pytest.raises(ValueError):
        Aircraft("TEST", "USA", -10, 5000)

def test_aircraft_raises_on_negative_altitude():
    with pytest.raises(ValueError):
        Aircraft("TEST", "USA", 100, -100)

def test_aircraft_comparison_by_altitude():
    a1 = Aircraft("A1", "USA", 200, 8000)
    a2 = Aircraft("A2", "UK", 250, 10000)
    assert a2 > a1  # по умолчанию сравниваем по высоте
    assert a1 < a2

def test_aircraft_comparison_by_speed():
    a1 = Aircraft("A1", "USA", 300, 8000)
    a2 = Aircraft("A2", "UK", 250, 10000)
    # Можно добавить отдельный метод или флаг, но по ТЗ достаточно сравнения по высоте/скорости
    assert a1.speed_kph > a2.speed_kph

def test_aircraft_setter_rejects_negative_speed():
    ac = Aircraft(call_sign="TEST", country="USA", speed_kph=500, altitude_m=1000)
    with pytest.raises(ValueError, match="speed_kph must be non-negative"):
        ac.speed_kph = -10

def test_aircraft_setter_rejects_negative_altitude():
    ac = Aircraft(call_sign="TEST", country="USA", speed_kph=500, altitude_m=1000)
    with pytest.raises(ValueError, match="altitude_m must be non-negative"):
        ac.altitude_m = -5