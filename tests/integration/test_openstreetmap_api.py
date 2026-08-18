from src.openstreetmap_api import OpenStreetMap

def test_openstreetmap_search() -> None:
    openstreetmap = OpenStreetMap()
    result = openstreetmap.search('Russia')
    assert isinstance(result, list)
    assert len(result) > 0
    first_result = result[0]
    assert first_result['name'] == 'Россия'