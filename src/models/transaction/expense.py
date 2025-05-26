from src.models.transaction.transaction import Transaction
from datetime import datetime
from typing import Optional
from src.models.category import Category
from src.models.payment_method.payment_method import PaymentMethod
from src.models.transaction.transaction_type import TransactionType


class Expense(Transaction):
    """
    Implementação concreta de Transaction para transações de saída/despesa.
    Pode ser parcelada (com número de parcelas) e associada a categorias.
    """

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
        """
        Inicializa uma despesa, que pode ser parcelada.

        Args:
            category: Categoria da despesa (alimentação, transporte, etc.)
            current_installment: Parcela atual (1 se não parcelado)
            total_installments: Total de parcelas (1 se não parcelado)
        """
        # Validações específicas de despesa
        if (current_installment and current_installment <= 0) or (
            total_installments and total_installments <= 0
        ):
            raise ValueError("Número de parcelas deve ser positivo")
        if (
            current_installment
            and total_installments
            and current_installment > total_installments
        ):
            raise ValueError("Parcela atual não pode ser maior que o total")

        super().__init__(id, amount, description, date, payment_method)
        self._category = category
        self._current_installment = current_installment
        self._total_installments = total_installments
        self._transaction_type = TransactionType.EXPENSE  # Define tipo específico

    # Propriedades específicas de despesa
    @property
    def category(self) -> Optional[Category]:
        """Getter para categoria da despesa"""
        return self._category

    @property
    def current_installment(self) -> int:
        """Getter para parcela atual"""
        return self._current_installment

    @property
    def total_installments(self) -> int:
        """Getter para total de parcelas"""
        return self._total_installments

    def to_dict(self) -> dict[str, any]:
        """Converte a despesa para dicionário"""
        return {
            "id": self._id,
            "amount": self._amount,
            "description": self._description,
            "date": self._date.isoformat(),
            "payment_method_id": (
                self._payment_method.id if self._payment_method else None
            ),
            "type": self._transaction_type,
            "category_id": self._category.id if self._category else None,
            "current_installment": self._current_installment,
            "total_installments": self._total_installments,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Expense":
        """Cria Expense a partir de dicionário"""
        return cls(
            id=data.get("id"),
            amount=data["amount"],
            description=data.get("description", ""),
            date=datetime.fromisoformat(data["date"]) if "date" in data else None,
            payment_method=(
                PaymentMethod(id=data.get("payment_method_id"))
                if data.get("payment_method_id")
                else None
            ),
            category=(
                Category(id=data.get("category_id"))
                if data.get("category_id")
                else None
            ),
            current_installment=data.get("current_installment", 1),
            total_installments=data.get("total_installments", 1),
        )
