from src.models.transaction.transaction import Transaction, TransactionType
from datetime import datetime
from typing import Optional
from src.models.payment_method.payment_method import PaymentMethod


class Income(Transaction):
    def __init__(
        self,
        id: Optional[int] = None,
        amount: float = 0.0,
        description: str = "",
        date: Optional[datetime] = None,
        payment_method: Optional[PaymentMethod] = None,
    ):
        super().__init__(id, amount, description, date, payment_method)

    @property
    def transaction_type(self) -> TransactionType:
        return TransactionType.INCOME

    def to_dict(self) -> dict[str, any]:
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            amount=data["amount"],
            description=data.get("description", ""),
            date=datetime.fromisoformat(data["date"]) if "date" in data else None,
            payment_method=data.get("payment_method"),
        )
