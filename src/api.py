from abc import ABC, abstractmethod
from typing import Any, Tuple, cast

import requests


class BaseApi(ABC):

    @property
    @abstractmethod
    def base_url(self) -> str: ...

    @abstractmethod
    def get_data(self, url: str, params: dict[str, Any]) -> list[dict[str, str]]: ...

    @staticmethod
    def get(url: str, params: dict[str, Any], headers: dict[str, str] | None = None) -> Any:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data


class OpenStreetMap(BaseApi):

    @property
    def base_url(self) -> str:
        return "https://nominatim.openstreetmap.org/"

    def get_data(self, url: str, params: dict[str, str]) -> list[dict[str, str]]:
        return cast(
            list[dict[str, str]],
            self.get(url, params=params, headers={"User-Agent": "sky-watch/1.0"}),
        )

    def search(self, country: str) -> list[dict[str, str]]:
        return self.get_data(
            f"{self.base_url}search",
            params={
                "country": country,
                "format": "jsonv2",
            },
        )

    def get_country_bbox(self, country: str) -> Tuple[float, float, float, float]:
        """Вернуть boundingbox страны в формате (south, north, west, east)."""
        data = self.search(country)
        if not data:
            raise ValueError(f"Страна '{country}' не найдена")
        south, north, west, east = map(float, data[0]["boundingbox"])
        return south, north, west, east


class OpenSky(BaseApi):

    @property
    def base_url(self) -> str:
        return "https://opensky-network.org/api/states/all"

    def get_data(self, url: str, params: dict[str, float]) -> list[dict[str, str]]:
        response = self.get(url, params=params)
        return cast(list[dict[str, str]], response["states"])

    def get_bbox(self, bbox: Tuple[float, float, float, float]) -> list[dict[str, str]]:
        south, north, west, east = bbox
        params = {"lamin": south, "lamax": north, "lomin": west, "lomax": east}
        return self.get_data(self.base_url, params)


class AeroplanesAPI:
    """Класс-фасад, объединяющий NominatimAPI и OpenSkyAPI."""

    def __init__(self) -> None:
        self._nominatim = OpenStreetMap()
        self._opensky = OpenSky()

    def get_aeroplanes(self, country: str) -> list[dict[str, str]]:
        """Вернуть список 'сырых' записей о самолётах в воздушном пространстве страны."""
        bbox = self._nominatim.get_country_bbox(country)
        return self._opensky.get_bbox(bbox)
