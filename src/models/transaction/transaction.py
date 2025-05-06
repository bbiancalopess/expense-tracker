from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional
from src.models.payment_method.payment_method import PaymentMethod


class TransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


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

        self.id = id
        self.amount = amount
        self.description = description
        self.date = date or datetime.now()
        self.payment_method = payment_method

    @property
    @abstractmethod
    def transaction_type(self) -> TransactionType:
        pass

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "date": self.date.isoformat(),
            "payment_method_id": (
                self.payment_method.id if self.payment_method else None
            ),
            "type": self.transaction_type.value,
        }
