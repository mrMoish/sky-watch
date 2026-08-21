from typing import Any


class Aeroplane:
    def __init__(
        self, callsign: str, origin_country: str, velocity: float | None = None, altitude: float | None = None
    ) -> None:
        self.callsign = callsign
        self.origin_country = origin_country
        self.velocity = velocity
        self.altitude = altitude

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        # есть самолеты у которых позывной пуст
        # if not isinstance(value, str) or not value.strip():
        # raise ValueError("Позывной некорректен")
        self._callsign = value.strip()

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @origin_country.setter
    def origin_country(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Страна регистрации должна быть непустой строкой")
        self._origin_country = value.strip()

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float | None) -> None:
        if value is None:
            raise ValueError("Информация о скорости отсутствует")
        value = float(value)
        if value < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self._velocity = value

    @property
    def altitude(self) -> float:
        return self._altitude

    @altitude.setter
    def altitude(self, value: float | None) -> None:
        # были случаи получения данных с отрицательной высотой
        if value is None:
            raise ValueError("Информация о высоте отсутствует")
        self._altitude = value

    def compare_speed(self, other: "Aeroplane") -> int:
        """Сравнить два самолёта по скорости. Возвращает -1, 0 или 1."""
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только объекты Aeroplane")
        if self.velocity < other.velocity:
            return -1
        if self.velocity > other.velocity:
            return 1
        return 0

    def compare_altitude(self, other: "Aeroplane") -> int:
        """Сравнить два самолёта по высоте полёта. Возвращает -1, 0 или 1."""
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только объекты Aeroplane")
        if self.altitude < other.altitude:
            return -1
        if self.altitude > other.altitude:
            return 1
        return 0

    @classmethod
    def cast_to_object_list(cls, data: list[list[Any]]) -> list["Aeroplane"]:
        """Преобразовать список 'сырых' записей OpenSky (states) в список объектов Aeroplane."""

        result: list[Aeroplane] = []
        for state in data:
            aeroplane = Aeroplane(
                callsign=state[1] or "N/A",
                origin_country=state[2] or "Unknown",
                velocity=state[9] or 0.0,
                altitude=state[7] or 0.0,
            )
            result.append(aeroplane)
        return result
    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для сохранения (например, в JSON)."""
        return {
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Aeroplane":
        """Создать объект Aeroplane из словаря (например, прочитанного из JSON)."""
        return cls(
            callsign=data.get("callsign", "N/A"),
            origin_country=data.get("origin_country", "Unknown"),
            velocity=data.get("velocity", 0.0),
            altitude=data.get("altitude", 0.0)
        )