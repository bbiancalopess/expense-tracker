class TransactionType:
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    @classmethod
    def get_types(cls) -> list[str]:
        return [cls.INCOME, cls.EXPENSE]

    @classmethod
    def validate(cls, transaction_type: str) -> bool:
        return transaction_type in cls.get_types()
