from abc import ABC
from typing import Optional


class Category(ABC):
    def __init__(self, id: Optional[int], name: str):
        self.id = id
        self.name = name

    def to_dict(self) -> dict[str, any]:
        return {"id": self.id, "name": self.name}
