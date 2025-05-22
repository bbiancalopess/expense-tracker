from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from src.models.payment_method.payment_method import PaymentMethod


class Transaction(ABC):
    def __init__(
        self,
        id: Optional[int] = None,
        amount: float = 0.0,
        description: str = "",
        date: Optional[datetime] = None,
        payment_method: Optional[PaymentMethod] = None,
    ):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self._id = id
        self._amount = amount
        self._description = description
        self._date = date or datetime.now()
        self._payment_method = payment_method
        self._transaction_type: str = ""

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def description(self) -> str:
        return self._description

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def payment_method(self) -> Optional[PaymentMethod]:
        return self._payment_method

    @property
    def transaction_type(self) -> str:
        return self._transaction_type

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, any]):
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, any]:
        pass
