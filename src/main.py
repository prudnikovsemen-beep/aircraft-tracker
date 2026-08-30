
# src/main.py
import argparse
import logging
from typing import List, Dict

from src.opensky_api import OpenSkyAPI
from src.nominatim_api import NominatimAPI
from src.aircraft import Aircraft

logger = logging.getLogger(__name__)


def get_top_n_by_altitude(
    n: int, bbox: Dict[str, float]
) -> List[Aircraft]:
    api = OpenSkyAPI()
    states = api.get_aircrafts_in_bbox(bbox)

    aircrafts: List[Aircraft] = []
    for s in states:
        try:
            ac = Aircraft.from_opensky_state(s)
            if ac.altitude_m > 0:
                aircrafts.append(ac)
        except ValueError:
            logger.warning("Skipping invalid aircraft data: %s", s.get("icao24"))
            continue

    aircrafts.sort(key=lambda a: a.altitude_m, reverse=True)
    return aircrafts[:n]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aircraft Tracker: show top N aircrafts by altitude"
    )
    parser.add_argument(
        "-n", "--top", type=int, default=10,
        help="Number of top aircrafts to show (default: 10)"
    )
    parser.add_argument(
        "--country", type=str, default=None,
        help="Country name to get BBOX via Nominatim (e.g. USA, Canada)"
    )
    args = parser.parse_args()

    if args.country:
        nominatim = NominatimAPI()
        bbox = nominatim.get_country_bbox(args.country)
        logger.info("Using BBOX for country %s: %s", args.country, bbox)
    else:
        bbox = {
            "south": 25.0,
            "north": 49.0,
            "west": -125.0,
            "east": -66.0,
        }
        logger.info("Using default BBOX (USA region)")

    top_aircrafts = get_top_n_by_altitude(args.top, bbox)

    if not top_aircrafts:
        print("No valid aircraft data found.")
        return

    print(f"Top {len(top_aircrafts)} aircrafts by altitude:")
    for i, ac in enumerate(top_aircrafts, start=1):
        print(
            f"{i}. {ac.call_sign} ({ac.country}) | "
            f"speed: {ac.speed_kph:.1f} km/h | "
            f"altitude: {ac.altitude_m:.0f} m"
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
