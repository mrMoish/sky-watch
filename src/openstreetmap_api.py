from abc import ABC, abstractmethod
from typing import cast, Tuple

import requests


class BaseApi(ABC):

    @abstractmethod
    def get_data(
        self, url: str, params: dict[str, str], headers: dict[str, str] | None = None
    ) -> list[dict[str, str]]: ...


class OpenStreetMap(BaseApi):

    BASE_URL = "https://nominatim.openstreetmap.org/"

    def get_data(
        self, url: str, params: dict[str, str], headers: dict[str, str] | None = None
    ) -> list[dict[str, str]]:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return cast(list[dict[str, str]], data)

    def search(self, country: str) -> list[dict[str, str]]:
        return self.get_data(
            f"{self.BASE_URL}search",
            params={
                "country": country,
                "format": "jsonv2",
            },
            headers={"User-Agent": "sky-watch/1.0"},
        )

    def get_country_bbox(self, country: str) -> Tuple[float, float, float, float]:
        """Вернуть boundingbox страны в формате (south, north, west, east)."""
        data = self.search(country)
        if not data:
            raise ValueError(f"Страна '{country}' не найдена")
        south, north, west, east = map(float, data[0]["boundingbox"])
        return south, north, west, east
