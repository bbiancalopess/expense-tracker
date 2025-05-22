# Abstract class
from abc import ABC, abstractmethod
from typing import Optional


class PaymentMethod(ABC):
    def __init__(self, id: Optional[int] = None, name: str = "", balance: float = 0.0):
        self._id = id
        self._name = name
        self._balance = balance
        self._payment_type: str = ""

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        if value is not None and value < 0:
            raise ValueError("ID cannot be negative")
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    @property
    def _payment_type(self) -> str:
        return self._payment_type

    @abstractmethod
    def to_dict(self) -> dict[str, any]:
        pass

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, any]):
        pass
