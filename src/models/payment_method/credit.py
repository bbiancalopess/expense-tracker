from src.models.payment_method.payment_method import PaymentMethod, PaymentType
from typing import Optional


class Credit(PaymentMethod):
    def __init__(
        self,
        id: Optional[int],
        name: str,
        balance: float = 0.0,
        credit_limit: float = 0.0,
        closing_date: int = None,
        due_date: int = None,
    ):
        super().__init__(id, name, balance)
        self.credit_limit = credit_limit
        self.closing_date = closing_date
        self.due_date = due_date

    @property
    def payment_type(self) -> PaymentType:
        return PaymentType.CREDIT

    @property
    def available_limit(self) -> float:
        return self.credit_limit - self.balance

    def process_payment(self, amount: float) -> bool:
        if amount > self.available_limit:
            return False
        self.balance += amount
        return True

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "credit_limit": self.credit_limit,
                "closing_date": self.closing_date,
                "due_date": self.due_date,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            balance=data.get("balance", 0),
            credit_limit=data.get("credit_limit", 0),
            closing_date=data.get("closing_date"),
            due_date=data.get("due_date"),
        )
