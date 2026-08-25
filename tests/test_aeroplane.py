from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane


def test_aeroplane() -> None:
    aeroplane = Aeroplane("   UAL1621", "United States",
                          268.79, 10203.18)
    assert aeroplane.callsign == "UAL1621"
    assert aeroplane.origin_country == "United States"
    assert aeroplane.velocity == 268.79
    assert aeroplane.altitude == 10203.18

    with pytest.raises(ValueError):
        Aeroplane("UAL1621", "", 268.79, 10203.18)
    with pytest.raises(ValueError):
        Aeroplane("UAL1621", "Russia", -268.79, 10203.18)
    with pytest.raises(ValueError):
        Aeroplane("UAL1621", "United States")
    with pytest.raises(ValueError):
        Aeroplane("UAL1621", "United States", 2253)


def test_cast_to_object_list() -> None:

    aeroplanes_api = AeroplanesAPI()
    data = aeroplanes_api.get_aeroplanes("USA")
    assert isinstance(data, list)
    assert len(data) > 0
    aeroplanes = Aeroplane.cast_to_object_list(data)
    assert isinstance(aeroplanes, list)
    assert len(aeroplanes) > 0

def test_compare_speed() -> None:
    plane1 = Aeroplane("ABC", "Russia", 500.0, 10000.0)
    plane2 = Aeroplane("DEF", "USA", 700.0, 10000.0)

    assert plane1.compare_speed(plane2) == -1
    assert plane2.compare_speed(plane1) == 1
    assert plane1.compare_speed(plane1) == 0


def test_compare_altitude() -> None:
    plane1 = Aeroplane("ABC", "Russia", 500.0, 10000.0)
    plane2 = Aeroplane("DEF", "USA", 500.0, 12000.0)

    assert plane1.compare_altitude(plane2) == -1
    assert plane2.compare_altitude(plane1) == 1
    assert plane1.compare_altitude(plane1) == 0

import pytest


def test_compare_speed_invalid_type() -> None:
    plane = Aeroplane("ABC", "Russia", 500.0, 10000.0)

    with pytest.raises(TypeError):
        plane.compare_speed("not an aeroplane") # type: ignore[arg-type]

def test_compare_altitude_invalid_type() -> None:
    plane = Aeroplane("ABC", "Russia", 500.0, 10000.0)

    with pytest.raises(TypeError):
        plane.compare_altitude("not an aeroplane") # type: ignore[arg-type]