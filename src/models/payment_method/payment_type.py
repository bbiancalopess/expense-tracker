class PaymentType:
    """
    Classe que define os tipos de pagamento disponíveis no sistema.
    """
    
    # Constantes de classe para tipos de pagamento
    CREDIT = "CREDIT"  # Pagamento via crédito
    DEBIT = "DEBIT"    # Pagamento via débito

    @classmethod
    def get_types(cls) -> list[str]:
        """Retorna lista com todos os tipos de pagamento disponíveis"""
        return [cls.CREDIT, cls.DEBIT]

    @classmethod
    def validate(cls, payment_type: str) -> bool:
        """Valida se um tipo de pagamento é válido"""
        return payment_type in cls.get_types()