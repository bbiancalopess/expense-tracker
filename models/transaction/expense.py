from models.transaction.transaction import Transaction
from datetime import date


class Expense(Transaction):
    def __init__(
        self,
        value: float,
        date: date,
        description: str,
        category: str,
        payment_method: str,
        id: int = None,
    ):
        super().__init__(value, date, description, category, payment_method, id)

    def type(self):
        return "expense"
