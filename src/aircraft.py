# src/aircraft.py
from __future__ import annotations
from typing import Any


class Aircraft:
    def __init__(
        self,
        call_sign: str,
        country: str,
        speed_kph: float,
        altitude_m: float,
    ) -> None:
        self.call_sign = call_sign
        self.country = country
        self._speed_kph = float(speed_kph)
        self._altitude_m = float(altitude_m)

        if self._speed_kph < 0:
            raise ValueError("speed_kph must be non-negative")
        if self._altitude_m < 0:
            raise ValueError("altitude_m must be non-negative")

    @property
    def speed_kph(self) -> float:
        return self._speed_kph

    @speed_kph.setter
    def speed_kph(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("speed_kph must be non-negative")
        self._speed_kph = value

    @property
    def altitude_m(self) -> float:
        return self._altitude_m

    @altitude_m.setter
    def altitude_m(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("altitude_m must be non-negative")
        self._altitude_m = value

    @classmethod
    def from_opensky_state(cls, state: dict[str, Any]) -> Aircraft:
        icao24 = state.get("icao24", "UNKNOWN")
        name = state.get("name", "")
        country = state.get("country", "Unknown")
        baro_alt = state.get("baro_altitude")
        geo_alt = state.get("geo_altitude")
        velocity_ms = state.get("velocity")

        altitude_m = (
            baro_alt
            if baro_alt is not None
            else (geo_alt if geo_alt is not None else 0.0)
        )
        speed_kph = (velocity_ms * 3.6) if velocity_ms is not None else 0.0

        call_sign = icao24 if icao24 != "UNKNOWN" else (name if name else "UNKNOWN")

        return cls(
            call_sign=call_sign,
            country=country,
            speed_kph=speed_kph,
            altitude_m=altitude_m,
        )

    def __repr__(self) -> str:
        return (
            f"Aircraft(call_sign={self.call_sign!r}, country={self.country!r}, "
            f"speed_kph={self.speed_kph:.1f}, altitude_m={self.altitude_m:.1f})"
        )

    def __lt__(self, other: Aircraft) -> bool:
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.altitude_m < other.altitude_m

    def __gt__(self, other: Aircraft) -> bool:
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.altitude_m > other.altitude_m
