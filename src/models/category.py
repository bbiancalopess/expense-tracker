from abc import ABC
from typing import Optional


class Category(ABC):
    def __init__(self, id: Optional[int], name: str):
        self._id = id
        self._name = name

    def to_dict(self) -> dict[str, any]:
        return {"id": self._id, "name": self._name}

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
