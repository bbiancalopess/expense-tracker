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
        self._id = id
        self._amount = amount
        self._description = description
        self._date = date or datetime.now()  # Data atual se não informada
        self._payment_method = payment_method
        self._transaction_type: str = ""  # Será definido nas subclasses

    # --- Propriedades e Setters ---
    @property
    def id(self) -> Optional[int]:
        """Getter para ID da transação"""
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        """Setter para ID"""
        self._id = value

    @property
    def amount(self) -> float:
        """Getter para valor da transação"""
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        """Setter para amount (valida se é positivo)"""
        if value <= 0:
            raise ValueError("Valor da transação deve ser positivo")
        self._amount = value

    @property
    def description(self) -> str:
        """Getter para descrição"""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Setter para description"""
        self._description = value

    @property
    def date(self) -> datetime:
        """Getter para data"""
        return self._date

    @date.setter
    def date(self, value: datetime) -> None:
        """Setter para date"""
        self._date = value

    @property
    def payment_method(self) -> Optional[PaymentMethod]:
        """Getter para método de pagamento"""
        return self._payment_method

    @payment_method.setter
    def payment_method(self, value: Optional[PaymentMethod]) -> None:
        """Setter para payment_method"""
        self._payment_method = value

    @property
    def transaction_type(self) -> str:
        """Getter para tipo de transação (apenas leitura)"""
        return self._transaction_type

    # --- Métodos ---
    def to_dict(self) -> dict[str, any]:
        """Converte transação para dicionário (serialização)"""
        return {
            "id": self._id,
            "amount": self._amount,
            "description": self._description,
            "date": self._date.isoformat(),
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
