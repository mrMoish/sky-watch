from abc import ABC, abstractmethod
from src.aeroplane import Aeroplane
import json
import os

class BaseStorage(ABC):

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить информацию о самолёте в хранилище."""
        ...

    @abstractmethod
    def get_aeroplanes(self, **criteria) -> list[Aeroplane]:
        """Получить самолёты из хранилища по указанным критериям."""
        ...

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удалить информацию о самолёте из хранилища."""
        ...


class JSONSaver(BaseStorage):
    """Хранилище данных о самолётах в JSON-файле."""

    def __init__(self, filepath: str = "data/aeroplanes.json"):
        self.filepath = filepath
        directory = os.path.dirname(self.filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.filepath):
            self._write_all([])

    def _read_all(self) -> list:
        with open(self.filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []

    def _write_all(self, data: list) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_all()
        data.append(aeroplane.to_dict())
        self._write_all(data)

    def get_aeroplanes(self, **criteria) -> list[Aeroplane]:
        data = self._read_all()
        aeroplanes = [Aeroplane.from_dict(item) for item in data]
        for key, value in criteria.items():
            aeroplanes = [a for a in aeroplanes if getattr(a, key, None) == value]
        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_all()
        data = [
            item
            for item in data
            if not (item.get("callsign") == aeroplane.callsign)
        ]
        self._write_all(data)