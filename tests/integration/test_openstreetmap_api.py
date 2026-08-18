from src.api import OpenStreetMap

def test_openstreetmap_search():
    openstreetmap = OpenStreetMap()
    result = openstreetmap.search('Moscow')
    assert isinstance(result, list)
    assert len(result) > 0
    first_result = result[0]
    assert first_result['name'] == 'Москва'