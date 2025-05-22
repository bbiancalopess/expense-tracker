from src.models.transaction.transaction import Transaction
from datetime import datetime
from typing import Optional
from src.models.category import Category
from src.models.payment_method.payment_method import PaymentMethod
from src.models.transaction.transaction_type import TransactionType


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
        if current_installment <= 0 or total_installments <= 0:
            raise ValueError("Installments must be positive")
        if current_installment > total_installments:
            raise ValueError("Current installment cannot be greater than total installments")

        super().__init__(id, amount, description, date, payment_method)
        self._category = category
        self._current_installment = current_installment
        self._total_installments = total_installments
        self._transaction_type = TransactionType.EXPENSE

    @property
    def category(self) -> Optional[Category]:
        return self._category

    @property
    def current_installment(self) -> int:
        return self._current_installment

    @property
    def total_installments(self) -> int:
        return self._total_installments

    def to_dict(self) -> dict[str, any]:
        return {
            "id": self._id,
            "amount": self._amount,
            "description": self._description,
            "date": self._date.isoformat(),
            "payment_method_id": self._payment_method._id if self._payment_method else None,
            "type": self._transaction_type,
            "category_id": self._category._id if self._category else None,
            "current_installment": self._current_installment,
            "total_installments": self._total_installments,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
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
