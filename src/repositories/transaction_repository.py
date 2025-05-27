from typing import Optional
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.models.transaction.transaction import Transaction
from src.models.transaction.income import Income
from src.models.transaction.expense import Expense
from src.models.transaction.transaction_type import TransactionType
from src.services.payment_method_service import PaymentMethodService
from src.services.category_service import CategoryService


class TransactionRepository:
    """
    Repositório para operações CRUD de transações financeiras.
    Lida com os tipos Income e Expense de forma transparente.
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.payment_method_service = PaymentMethodService()
        self.category_service = CategoryService()

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
            payment_method = None
            if data.get("payment_method_id"):
                payment_method = self.payment_method_service.get_payment_method_by_id(
                    data["payment_method_id"]
                )

            category = None
            if data.get("category_id"):
                category = self.category_service.get_category_by_id(data["category_id"])

            if data["type"] == TransactionType.INCOME:
                return Income(
                    id=data.get("id"),
                    amount=data["amount"],
                    description=data.get("description", ""),
                    date=(
                        datetime.fromisoformat(data["date"]) if "date" in data else None
                    ),
                    payment_method=payment_method,
                )
            elif data["type"] == TransactionType.EXPENSE:
                return Expense(
                    id=data.get("id"),
                    amount=data["amount"],
                    description=data.get("description", ""),
                    date=(
                        datetime.fromisoformat(data["date"]) if "date" in data else None
                    ),
                    payment_method=payment_method,
                    category=category,
                    current_installment=data.get("current_installment", 1),
                    total_installments=data.get("total_installments", 1),
                )
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

            if isinstance(transaction, Expense):
                if transaction.payment_method:
                    data["payment_method_id"] = transaction.payment_method.id
                if transaction.category:
                    data["category_id"] = transaction.category.id

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
                    data.get("payment_method_id", None),
                    data.get("category_id", None),
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

    def get_current_month_totals_by_payment_method(self) -> dict[int, dict[str, float]]:
        """
        Retorna os totais de incomes e expenses do mês atual agrupados por payment_method.

        Returns:
            Dict[int, Dict[str, float]]:
            - Chave: payment_method_id
            - Valor: Dicionário com:
                - 'income': soma total de incomes do mês
                - 'expense': soma total de expenses do mês
        """
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            query = """
                SELECT 
                    payment_method_id,
                    SUM(CASE WHEN type = ? THEN amount ELSE 0 END) as income_total,
                    SUM(CASE WHEN type = ? THEN amount ELSE 0 END) as expense_total
                FROM transactions
                WHERE payment_method_id IS NOT NULL
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?
                GROUP BY payment_method_id;
            """
            params = (
                TransactionType.INCOME,
                TransactionType.EXPENSE,
                f"{current_month:02d}",
                str(current_year),
            )

            results = self.db.select(query, params)

            return {
                row["payment_method_id"]: {
                    "income": row["income_total"] or 0.0,
                    "expense": row["expense_total"] or 0.0,
                }
                for row in results
            }

        except Exception as e:
            raise Exception(f"Error getting current month transaction totals: {e}")
