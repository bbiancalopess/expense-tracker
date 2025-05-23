from typing import Optional
from src.database.db_manager import DatabaseManager
from src.models.transaction.transaction import Transaction
from src.models.transaction.income import Income
from src.models.transaction.expense import Expense
from src.models.transaction.transaction_type import TransactionType


class TransactionRepository:
    """
    Repositório para operações CRUD de transações financeiras.
    Lida com os tipos Income e Expense de forma transparente.
    """

    def __init__(self, db: DatabaseManager):
        self.db = db

    def __create_transaction_from_dict(self, data: dict) -> Optional[Transaction]:
        """
        Factory method interno para criar instâncias específicas de Transaction.

        Args:
            data: Dicionário com os dados do banco

        Returns:
            Instância de Income, Expense ou None se inválido
        """
        if not data or "type" not in data:
            return None

        try:
            if data["type"] == TransactionType.INCOME:
                return Income.from_dict(data)
            elif data["type"] == TransactionType.EXPENSE:
                return Expense.from_dict(data)
            return None
        except Exception as e:
            raise Exception(f"Error creating transaction from dict: {e}")

    def get_all(self) -> list[Transaction]:
        """
        Recupera todas as transações do banco.

        Returns:
            Lista de Transaction (Income ou Expense) ou lista vazia
        """
        try:
            query = """
                SELECT id, amount, description, date,
                       payment_method_id, category_id,
                       current_installment, total_installments, type
                FROM transactions
                ORDER BY date DESC;
            """
            results = self.db.select(query)
            return (
                [self.__create_transaction_from_dict(row) for row in results]
                if results
                else []
            )
        except Exception as e:
            raise Exception(f"Error getting all transactions: {e}")

    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """
        Busca uma transação pelo ID.

        Args:
            transaction_id: ID da transação

        Returns:
            Instância de Transaction ou None se não encontrada
        """
        try:
            query = """
                SELECT id, amount, description, date,
                       payment_method_id, category_id,
                       current_installment, total_installments, type
                FROM transactions
                WHERE id = ?;
            """
            result = self.db.select_one(query, (transaction_id,))
            return self.__create_transaction_from_dict(result) if result else None
        except Exception as e:
            raise Exception(f"Error getting transaction by ID {transaction_id}: {e}")

    def save(self, transaction: Transaction) -> int:
        """
        Salva uma transação no banco (insere ou atualiza).

        Args:
            transaction: Instância de Income ou Expense

        Returns:
            ID da transação salva ou None em caso de falha

        Raises:
            ValueError: Se o objeto transaction for inválido
        """
        if not isinstance(transaction, Transaction):
            raise ValueError("Invalid transaction object")

        try:
            data = transaction.to_dict()

            if transaction.id:
                # Atualização
                query = """
                    UPDATE transactions SET
                    amount = ?, description = ?, date = ?,
                    payment_method_id = ?, category_id = ?,
                    current_installment = ?, total_installments = ?
                    WHERE id = ?;
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
                return transaction.id
            else:
                # Inserção
                query = """
                    INSERT INTO transactions (
                        amount, description, date, payment_method_id,
                        category_id, current_installment, total_installments, type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
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
            raise Exception(f"Error saving transaction: {e}")

    def delete(self, transaction_id: int) -> bool:
        """
        Remove uma transação do banco.

        Args:
            transaction_id: ID da transação a ser removida

        Returns:
            True se removida com sucesso, False caso contrário
        """
        try:
            query = "DELETE FROM transactions WHERE id = ?;"
            return self.db.delete(query, (transaction_id,)) > 0
        except Exception as e:
            raise Exception(f"Error deleting transaction {transaction_id}: {e}")
