import requests
from abc import ABC, abstractmethod

class BaseApi(ABC):

    @abstractmethod
    def get_data(self, url: str, params: dict, headers: dict|None=None) -> list:
        ...


class OpenStreetMap(BaseApi):

    BASE_URL = 'https://nominatim.openstreetmap.org/'

    def get_data(self, url, params: dict, headers: dict|None=None) -> list:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data

    def search(self, country: str) -> list:
        return self.get_data(f"{self.BASE_URL}search",
                             params={"country": country,
                                     'format': 'jsonv2',},
                             headers= {"User-Agent": "sky-watch/1.0"})