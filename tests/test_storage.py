from src.storage import JSONSaver
from src.aeroplane import Aeroplane

def test_storage() -> None:
    __import__('pathlib').Path('data/aeroplanes.json').unlink(missing_ok=True)
    aeroplane = Aeroplane("   UAL1621", "United States",
                          268.79, 10203.18)
    storage = JSONSaver()
    storage.add_aeroplane(aeroplane)
    get_list = storage.get_aeroplanes(origin_country="United States")
    assert len(get_list) > 0
    result = get_list[0]
    assert result.callsign ==  aeroplane.callsign
    assert result.origin_country == aeroplane.origin_country
    assert result.velocity == aeroplane.velocity
    assert result.altitude == aeroplane.altitude


    storage.delete_aeroplane(aeroplane)