# Abstract class
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class PaymentType(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class PaymentMethod(ABC):
    def __init__(self, id: Optional[int] = None, name: str = "", balance: float = 0.0):
        self._id = id
        self._name = name
        self._balance = balance

    @abstractmethod
    def payment_type(self) -> PaymentType:
        pass

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self._id,
            "name": self._name,
            "balance": self._balance,
            "type": self.payment_type.value,
        }

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass
