from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from src.models.payment_method.payment_method import PaymentMethod


class Transaction(ABC):
    """
    Classe abstrata que representa uma transação financeira genérica.
    Pode ser uma despesa (Expense) ou receita (Income).
    """

    def __init__(
        self,
        id: Optional[int] = None,
        amount: float = 0.0,
        description: str = "",
        date: Optional[datetime] = None,
        payment_method: Optional[PaymentMethod] = None,
    ):
        """
        Inicializa uma transação com dados básicos.

        Args:
            amount: Valor da transação (deve ser positivo)
            description: Descrição/observação
            date: Data (usa data atual se não informada)
            payment_method: Método de pagamento associado
        """
        if amount <= 0:
            raise ValueError("Valor da transação deve ser positivo")

        self._id = id
        self._amount = amount
        self._description = description
        self._date = date or datetime.now()  # Data atual se não informada
        self._payment_method = payment_method
        self._transaction_type: str = ""  # Será definido nas subclasses

    # Propriedades básicas
    @property
    def id(self) -> Optional[int]:
        """Getter para ID da transação"""
        return self._id

    @property
    def amount(self) -> float:
        """Getter para valor da transação"""
        return self._amount

    @property
    def description(self) -> str:
        """Getter para descrição"""
        return self._description

    @property
    def date(self) -> datetime:
        """Getter para data"""
        return self._date

    @property
    def payment_method(self) -> Optional[PaymentMethod]:
        """Getter para método de pagamento"""
        return self._payment_method

    @property
    def transaction_type(self) -> str:
        """Getter para tipo de transação"""
        return self._transaction_type

    # Métodos abstratos
    @abstractmethod
    def to_dict(self) -> dict[str, any]:
        """Converte transação para dicionário (serialização)"""
        return {
            "id": self._id,
            "amount": self._amount,
            "description": self._description,
            "date": self._date.isoformat(),  # Converte data para string ISO
            "payment_method_id": (
                self._payment_method.id if self._payment_method else None
            ),
            "type": self._transaction_type,
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, any]) -> "Transaction":
        """Cria transação a partir de dicionário (desserialização)"""
        pass
