from abc import ABC, abstractmethod
from typing import Optional


class PaymentMethod(ABC):
    """
    Classe abstrata que representa um método de pagamento genérico.
    Serve como base para implementações específicas como crédito e débito.
    """

    def __init__(self, id: Optional[int] = None, name: str = "", balance: float = 0.0):
        """
        Inicializa o método de pagamento com valores básicos.

        Args:
            id: Identificador único (opcional)
            name: Nome do método de pagamento
            balance: Saldo/valor disponível
        """
        self._id = id  # ID interno
        self._name = name  # Nome do método
        self._balance = balance  # Saldo disponível
        self._payment_type: str = ""  # Tipo (será definido nas subclasses)

    # Propriedades com validação
    @property
    def id(self) -> Optional[int]:
        """Getter para o ID do método de pagamento"""
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        """Setter para ID com validação"""
        if value is not None and value < 0:
            raise ValueError("ID não pode ser negativo")
        self._id = value

    @property
    def name(self) -> str:
        """Getter para o nome do método"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setter para nome com validação"""
        if not value.strip():
            raise ValueError("Nome não pode ser vazio")
        self._name = value

    @property
    def balance(self) -> float:
        """Getter para o saldo/disponível"""
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        """Setter para saldo com validação"""
        if value < 0:
            raise ValueError("Saldo não pode ser negativo")
        self._balance = value

    @property
    def payment_type(self) -> str:
        """Getter para o tipo de pagamento"""
        return self._payment_type

    # Métodos abstratos que devem ser implementados pelas subclasses
    def to_dict(self) -> dict[str, any]:
        """Converte o objeto para dicionário (serialização)"""
        return {
            "id": self._id,
            "name": self._name,
            "balance": self._balance,
            "type": self._payment_type,
        }

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Processa um pagamento com o valor especificado"""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, any]):
        """Cria instância a partir de dicionário (desserialização)"""
        pass
