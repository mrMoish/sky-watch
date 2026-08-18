import pytest

from src.openstreetmap_api import OpenStreetMap


def test_openstreetmap_search() -> None:
    openstreetmap = OpenStreetMap()
    result = openstreetmap.search("Russia")
    assert isinstance(result, list)
    assert len(result) > 0
    first_result = result[0]
    assert first_result["name"] == "Россия"

def test_openstreetmap_get_boundingbox() -> None:
    openstreetmap = OpenStreetMap()
    bbox = openstreetmap.get_country_bbox("Argentina")
    assert bbox == (-55.1925709, -21.7808568, -73.5605371, -53.6374515)

def test_openstreetmap_get_boundingbox_with_error() -> None:
    openstreetmap = OpenStreetMap()
    with pytest.raises(ValueError):
        openstreetmap.get_country_bbox("Moscow")
