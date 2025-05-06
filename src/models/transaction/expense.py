from src.models.transaction.transaction import Transaction, TransactionType
from datetime import datetime
from typing import Optional
from src.models.category import Category
from src.models.payment_method.payment_method import PaymentMethod


class Expense(Transaction):
    def __init__(
        self,
        id: Optional[int] = None,
        amount: float = 0.0,
        description: str = "",
        date: Optional[datetime] = None,
        payment_method: Optional[PaymentMethod] = None,
        category: Optional[Category] = None,
        current_installment: int = 1,
        total_installments: int = 1,
    ):
        super().__init__(id, amount, description, date, payment_method)
        self.category = category
        self.current_installment = current_installment
        self.total_installments = total_installments

    @property
    def transaction_type(self) -> TransactionType:
        return TransactionType.EXPENSE

    def to_dict(self) -> dict[str, any]:
        data = super().to_dict()
        data.update(
            {
                "category_id": self.category.id if self.category else None,
                "current_installment": self.current_installment,
                "total_installments": self.total_installments,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            amount=data["amount"],
            description=data.get("description", ""),
            date=datetime.fromisoformat(data["date"]) if "date" in data else None,
            payment_method=data.get("payment_method"),
            category=data.get("category"),
            current_installment=data.get("current_installment", 1),
            total_installments=data.get("total_installments", 1),
        )
