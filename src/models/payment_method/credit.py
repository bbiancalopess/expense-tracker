from src.models.payment_method.payment_method import PaymentMethod, PaymentType
from typing import Optional
from src.models.payment_method.payment_type import PaymentType


class Credit(PaymentMethod):
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        balance: float = 0.0,
        credit_limit: float = 0.0,
        closing_day: Optional[int] = None,
        due_day: Optional[int] = None,
    ):
        super().__init__(id, name, balance)
        self._credit_limit = credit_limit
        self._closing_day = closing_day
        self._due_day = due_day
        self._payment_type = PaymentType.CREDIT

    @property
    def credit_limit(self) -> float:
        return self._credit_limit

    @credit_limit.setter
    def credit_limit(self, value: float) -> None:
        if value < 0:
            raise ValueError("Credit limit cannot be negative")
        self._credit_limit = value

    @property
    def closing_day(self) -> Optional[int]:
        return self._closing_day

    @closing_day.setter
    def closing_day(self, value: Optional[int]) -> None:
        if value is not None and (value < 1 or value > 31):
            raise ValueError("Closing day must be between 1 and 31")
        self._closing_day = value

    @property
    def due_day(self) -> Optional[int]:
        return self._due_day

    @due_day.setter
    def due_day(self, value: Optional[int]) -> None:
        if value is not None and (value < 1 or value > 31):
            raise ValueError("Due day must be between 1 and 31")
        self._due_day = value

    @property
    def available_limit(self) -> float:
        return self._credit_limit - self._balance

    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        if amount > self.available_limit:
            return False
        self._balance += amount
        return True

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self._id,
            "name": self._name,
            "balance": self._balance,
            "type": self._payment_type,
            "credit_limit": self._credit_limit,
            "closing_day": self._closing_day,
            "due_day": self._due_day,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> 'Credit':
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            balance=data.get("balance", 0.0),
            credit_limit=data.get("credit_limit", 0.0),
            closing_day=data.get("closing_day"),
            due_day=data.get("due_day"),
        )
