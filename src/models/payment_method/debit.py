from src.models.payment_method.payment_method import PaymentMethod, PaymentType
from typing import Optional


class Debit(PaymentMethod):
    def __init__(
        self,
        id: Optional[int],
        name: str,
        balance: float = 0.0,
    ):
        super().__init__(id, name, balance)

    @property
    def payment_type(self) -> PaymentType:
        return PaymentType.DEBIT

    def process_payment(self, amount: float) -> bool:
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def to_dict(self):
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"), name=data.get("name", ""), balance=data.get("balance", 0)
        )

    @property
    def id(self):
        return self._id

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        """Setter para o saldo com validações"""
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
