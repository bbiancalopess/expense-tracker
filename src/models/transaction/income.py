from src.models.transaction.transaction import Transaction
from datetime import datetime
from typing import Optional
from src.models.payment_method.payment_method import PaymentMethod
from src.models.transaction.transaction_type import TransactionType


class Income(Transaction):
    """
    Implementação concreta de Transaction para transações de entrada/receita.
    Exemplos: Salário, reembolsos, transferências recebidas, etc.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        amount: float = 0.0,
        description: str = "",
        date: Optional[datetime] = None,
        payment_method: Optional[PaymentMethod] = None,
    ):
        """Inicializa uma receita financeira"""
        super().__init__(id, amount, description, date, payment_method)
        self._transaction_type = TransactionType.INCOME  # Define tipo específico

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Income":
        """Cria Income a partir de dicionário"""
        payment_method = data.get("payment_method")

        if not payment_method and "payment_method_id" in data:
            payment_method = PaymentMethod(id=data["payment_method_id"])

        return cls(
            id=data.get("id"),
            amount=data["amount"],
            description=data.get("description", ""),
            date=datetime.fromisoformat(data["date"]) if "date" in data else None,
            payment_method=payment_method,
        )
