# tests/test_nominatim_api.py
import responses
from src.nominatim_api import NominatimAPI

@responses.activate
def test_nominatim_get_country_bbox_returns_bbox():
    # Регистрируем точный запрос: со всеми параметрами, включая limit=1
    responses.add(
        responses.GET,
        "https://nominatim.openstreetmap.org/search",
        match=[
            responses.matchers.query_param_matcher({
                "q": "Canada",
                "format": "json",
                "limit": "1",
            })
        ],
        json=[
            {
                "boundingbox": ["41.680561", "83.110699", "-141.002754", "-52.648098"],
                "display_name": "Canada",
            }
        ],
        status=200,
    )

    api = NominatimAPI()
    bbox = api.get_country_bbox("Canada")

    assert bbox["south"] == 41.680561
    assert bbox["north"] == 83.110699
    assert bbox["west"] == -141.002754
    assert bbox["east"] == -52.648098
