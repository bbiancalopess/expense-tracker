from src.models.payment_method.payment_method import PaymentMethod
from src.models.payment_method.payment_type import PaymentType
from typing import Optional


class Debit(PaymentMethod):
    """
    Implementação concreta de PaymentMethod para cartões de débito.
    Mais simples que o crédito, apenas verifica saldo disponível.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        balance: float = 0.0,
    ):
        """Inicializa cartão de débito com saldo disponível"""
        super().__init__(id, name, balance)
        self._payment_type = PaymentType.DEBIT  # Define tipo específico

    def process_payment(self, amount: float) -> bool:
        """
        Processa pagamento no débito.

        Args:
            amount: Valor a ser debitado

        Returns:
            bool: True se pagamento aprovado (saldo suficiente), False caso contrário

        Raises:
            ValueError: Se valor for inválido
        """
        if amount <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        if amount > self._balance:
            return False  # Saldo insuficiente
        self._balance -= amount  # Debita do saldo
        return True  # Pagamento aprovado

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Debit":
        """Cria instância de Debit a partir de dicionário"""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            balance=data.get("balance", 0.0),
        )
