from src.repositories.transaction_repository import TransactionRepository
from src.models.transaction.transaction import Transaction
from typing import Optional
from src.models.transaction.expense import Expense


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repo = repository

    def add_transaction(self, transaction: Transaction) -> Transaction:
        if isinstance(transaction, Expense) and not transaction.category:
            print("Expense must have a category")
            return None

        try:
            transaction_id = self.repo.save(transaction)
            if transaction_id:
                transaction.id = transaction_id
                return transaction
            return None
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None

    def get_all_transactions(self) -> list[Transaction]:
        try:
            return self.repo.get_all()
        except Exception as e:
            print(f"Error getting all transactions service: {e}")
            return []

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        if transaction_id <= 0:
            return None

        try:
            return self.repo.get_by_id(transaction_id)
        except Exception as e:
            print(f"Error getting transaction by ID {transaction_id}: {e}")
            return None

    def update_transaction(self, transaction: Transaction) -> bool:
        try:
            return self.repo.save(transaction) is not None
        except Exception as e:
            print(f"Error updating transaction {transaction.id}: {e}")
            return False

    def delete_transaction(self, transaction_id: int) -> bool:
        if transaction_id <= 0:
            return False

        try:
            return self.repo.delete(transaction_id)
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False
