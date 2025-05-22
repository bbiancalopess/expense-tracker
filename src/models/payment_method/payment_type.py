class PaymentType:
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

    @classmethod
    def get_types(cls) -> list[str]:
        return [cls.CREDIT, cls.DEBIT]

    @classmethod
    def validate(cls, payment_type: str) -> bool:
        return payment_type in cls.get_types()
