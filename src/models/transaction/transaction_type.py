class TransactionType:
    """
    Classe que define os tipos de transação financeira.
    Similar ao PaymentType mas para classificar transações.
    """

    # Constantes de classe
    INCOME = "INCOME"  # Transação de entrada/receita
    EXPENSE = "EXPENSE"  # Transação de saída/despesa

    @classmethod
    def get_types(cls) -> list[str]:
        """Retorna todos os tipos de transação disponíveis"""
        return [cls.INCOME, cls.EXPENSE]

    @classmethod
    def validate(cls, transaction_type: str) -> bool:
        """Verifica se um tipo de transação é válido"""
        return transaction_type in cls.get_types()
