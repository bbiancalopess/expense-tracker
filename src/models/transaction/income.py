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

    def to_dict(self) -> dict[str, any]:
        """Converte a receita para dicionário"""
        return {
            "id": self._id,
            "amount": self._amount,
            "description": self._description,
            "date": self._date.isoformat(),  # Converte data para string ISO
            "payment_method_id": self._payment_method.id if self._payment_method else None,
            "type": self._transaction_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> 'Income':
        """Cria Income a partir de dicionário"""
        return cls(
            id=data.get("id"),
            amount=data["amount"],
            description=data.get("description", ""),
            date=datetime.fromisoformat(data["date"]) if "date" in data else None,
            payment_method=data.get("payment_method"),
        )
