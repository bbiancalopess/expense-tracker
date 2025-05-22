from src.models.payment_method.payment_method import PaymentMethod
from src.models.payment_method.payment_type import PaymentType
from typing import Optional


class Debit(PaymentMethod):
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        balance: float = 0.0,
    ):
        super().__init__(id, name, balance)
        self._payment_type = PaymentType.DEBIT

    def process_payment(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        if amount > self.balance:
            return False
        self._balance -= amount
        return True

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self._id,
            "name": self._name,
            "balance": self._balance,
            "type": self._payment_type,
        }

    def from_dict(self, data: dict[str, any]) -> 'Debit':
        return self(
            id=data.get("id"),
            name=data.get("name", ""),
            balance=data.get("balance", 0),
        )
