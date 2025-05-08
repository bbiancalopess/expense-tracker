from typing import Optional
from src.database.db_manager import DatabaseManager
from src.models.transaction.transaction import Transaction, TransactionType
from src.models.transaction.income import Income
from src.models.transaction.expense import Expense


class TransactionRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def __create_transaction_from_dict(self, data: dict) -> Optional[Transaction]:
        if not data:
            return None

        try:
            if data.get("type") == TransactionType.INCOME.value:
                return Income.from_dict(data)
            elif data.get("type") == TransactionType.EXPENSE.value:
                return Expense.from_dict(data)
            return None
        except Exception as err:
            print(f"Error creating transaction from dict: {err}")
            return None

    def get_all(self) -> list[Transaction]:
        try:
            query = "SELECT * FROM transactions;"
            results = self.db.select(query)
            if not results:
                return []

            return [self.__create_transaction_from_dict(row) for row in results]
        except Exception as e:
            print(f"Error getting all transactions: {e}")
            return []

    def get_by_id(self, payment_id: int) -> Optional[Transaction]:
        try:
            query = "SELECT * FROM transactions WHERE id = ?;"
            result = self.db.select_one(query, (payment_id,))
            if not result:
                return None

            return self.__create_transaction_from_dict(result)
        except Exception as e:
            print(f"Error getting transaction by ID {payment_id}: {e}")
            return None

    def save(self, transaction: Transaction) -> int:
        try:
            data = transaction.to_dict()

            if transaction._id:
                query = """
                    UPDATE transactions SET
                    amount=?, description=?, date=?,
                    payment_method_id=?, category_id=?,
                    current_installment=?, total_installments=?
                    WHERE id=?
                """
                params = (
                    data["amount"],
                    data["description"],
                    data["date"],
                    data["payment_method_id"],
                    data.get("category_id"),
                    data.get("current_installment", 1),
                    data.get("total_installments", 1),
                    data["id"],
                )
                self.db.update(query, params)
                return transaction._id
            else:
                query = """
                    INSERT INTO transactions (
                        amount, description, date, payment_method_id,
                        category_id, current_installment, total_installments, type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    data["amount"],
                    data["description"],
                    data["date"],
                    data["payment_method_id"],
                    data.get("category_id"),
                    data.get("current_installment", 1),
                    data.get("total_installments", 1),
                    data["type"],
                )
                return self.db.insert(query, params)
        except Exception as e:
            print(f"Error saving transaction: {e}")
            return None

    def delete(self, transaction_id: int) -> bool:
        try:
            query = "DELETE FROM transactions WHERE id = ?;"
            return self.db.delete(query, (transaction_id,)) > 0
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False
