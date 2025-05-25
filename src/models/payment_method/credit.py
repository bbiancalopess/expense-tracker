from src.models.payment_method.payment_method import PaymentMethod
from typing import Optional
from src.models.payment_method.payment_type import PaymentType


class Credit(PaymentMethod):
    """
    Implementação concreta de PaymentMethod para cartões de crédito.
    Adiciona funcionalidades específicas como limite de crédito e datas de vencimento.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        balance: float = 0.0,
        credit_limit: float = 0.0,
        closing_day: Optional[int] = None,
        due_day: Optional[int] = None,
    ):
        """
        Inicializa um cartão de crédito com características específicas.

        Args:
            credit_limit: Limite total do cartão
            closing_day: Dia de fechamento da fatura
            due_day: Dia de vencimento do pagamento
        """
        super().__init__(id, name, balance)
        self._credit_limit = credit_limit
        self._closing_day = closing_day
        self._due_day = due_day
        self._payment_type = PaymentType.CREDIT  # Define o tipo específico

    # Propriedades específicas do crédito
    @property
    def credit_limit(self) -> float:
        """Getter para o limite de crédito"""
        return self._credit_limit

    @credit_limit.setter
    def credit_limit(self, value: float) -> None:
        """Setter para limite com validação"""
        if value < 0:
            raise ValueError("Limite não pode ser negativo")
        self._credit_limit = value

    @property
    def closing_day(self) -> Optional[int]:
        """Getter para dia de fechamento"""
        return self._closing_day

    @closing_day.setter
    def closing_day(self, value: Optional[int]) -> None:
        """Setter para dia de fechamento com validação (1-31)"""
        if value is not None and not (1 <= value <= 31):
            raise ValueError("Dia de fechamento deve ser entre 1 e 31")
        self._closing_day = value

    @property
    def due_day(self) -> Optional[int]:
        """Getter para dia de vencimento"""
        return self._due_day

    @due_day.setter
    def due_day(self, value: Optional[int]) -> None:
        """Setter para dia de vencimento com validação (1-31)"""
        if value is not None and not (1 <= value <= 31):
            raise ValueError("Dia de vencimento deve ser entre 1 e 31")
        self._due_day = value

    @property
    def available_limit(self) -> float:
        """Calcula o limite disponível (limite total - saldo utilizado)"""
        return self._credit_limit - self._balance

    def process_payment(self, amount: float) -> bool:
        """
        Processa um pagamento no crédito.

        Args:
            amount: Valor a ser cobrado

        Returns:
            bool: True se pagamento foi aprovado, False se recusado

        Raises:
            ValueError: Se valor for inválido
        """
        if amount <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        if amount > self.available_limit:
            return False  # Limite insuficiente
        self._balance += amount  # Atualiza o saldo utilizado
        return True  # Pagamento aprovado

    def to_dict(self) -> dict[str, any]:
        """Converte o cartão para dicionário serializável"""
        return {
            "id": self._id,
            "name": self._name,
            "balance": self._balance,
            "type": self._payment_type,
            "credit_limit": self._credit_limit,
            "closing_day": self._closing_day,
            "due_day": self._due_day,
        }

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Credit":
        """Cria instância de Credit a partir de dicionário"""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            balance=data.get("balance", 0.0),
            credit_limit=data.get("credit_limit", 0.0),
            closing_day=data.get("closing_day"),
            due_day=data.get("due_day"),
        )
