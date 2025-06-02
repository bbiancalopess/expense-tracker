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
        try:
            query = "DELETE FROM transactions WHERE id = ?;"
            return self.db.delete(query, (transaction_id,)) > 0
        except Exception as e:
            raise Exception(f"Error deleting transaction {transaction_id}: {e}")

    def get_current_month_totals_by_payment_method(self) -> dict[int, dict[str, float]]:
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

    def get_total_expenses_for_current_month(self) -> float:
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            query = """
                SELECT
                    SUM(amount) as total
                FROM transactions
                WHERE type = ?
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?;
            """
            params = (
                TransactionType.EXPENSE,
                f"{current_month:02d}",
                str(current_year),
            )

            results = self.db.select_one(query, params)

            return results["total"] if results and results.get("total") else 0.0

        except Exception as e:
            raise Exception(f"Error getting current month transaction totals: {e}")

    def get_most_added_category_for_current_month(self) -> str:
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            query = """
                SELECT
                    c.name,
                    SUM(t.amount) as total_spent
                FROM transactions t
                JOIN categories c ON c.id = t.category_id
                WHERE type = ?
                AND strftime('%m', date) = ?
                AND strftime('%Y', date) = ?
                GROUP BY t.category_id
                ORDER BY total_spent DESC
                LIMIT 1;
            """
            params = (
                TransactionType.EXPENSE,
                f"{current_month:02d}",
                str(current_year),
            )

            results = self.db.select_one(query, params)

            return results["name"] if results and results.get("name") else ""

        except Exception as e:
            raise Exception(f"Error getting current month transaction totals: {e}")

    def count_month_transactions(self) -> int:
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            query = """
                SELECT COUNT(id) as total_transactions
                FROM transactions
                WHERE strftime('%m', date) = ?
                AND strftime('%Y', date) = ?;
            """
            params = (
                f"{current_month:02d}",
                str(current_year),
            )

            result = self.db.select_one(query, params)
            return result["total_transactions"] if result else 0

        except Exception as e:
            raise Exception(f"Error getting current month transaction totals: {e}")

    def get_expenses_per_category_for_current_month(self) -> list[dict]:
        try:
            current_month = datetime.now().month
            current_year = datetime.now().year

            query = """
                SELECT
                    SUM(t.amount) as total_expense,
                    c.name
                FROM transactions t
                JOIN categories c ON c.id = t.category_id
                WHERE t.type = ?
                AND strftime('%m', t.date) = ?
                AND strftime('%Y', t.date) = ?
                GROUP BY t.category_id;
            """
            params = (
                TransactionType.EXPENSE,
                f"{current_month:02d}",
                str(current_year),
            )

            results = self.db.select(query, params)
            return [
                {"name": row["name"], "total_expense": row["total_expense"]}
                for row in results
            ]

        except Exception as e:
            raise Exception(f"Error getting expenses per category: {e}")

    def get_monthly_expenses(self) -> list[dict]:
        try:
            query = """
                SELECT 
                    strftime('%m/%Y', date) as month,
                    SUM(amount) as total
                FROM transactions
                WHERE type = ?
                    AND date >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', date)
                ORDER BY date ASC;
            """
            results = self.db.select(query, (TransactionType.EXPENSE,))
            return [{"month": row["month"], "total": row["total"]} for row in results]
        except Exception as e:
            raise Exception(f"Error getting monthly expenses: {e}")

    def get_category_stats(self) -> dict:
        try:
            # Categoria mais usada
            query_most_used = """
                SELECT c.name, COUNT(t.id) as count
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.type = ?
                GROUP BY t.category_id
                ORDER BY count DESC
                LIMIT 1;
            """
            most_used = self.db.select_one(query_most_used, (TransactionType.EXPENSE,))

            # Todas as categorias com contagem
            query_all = """
                SELECT c.name, COUNT(t.id) as count
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.type = ?
                GROUP BY t.category_id;
            """
            all_categories = self.db.select(query_all, (TransactionType.EXPENSE,))

            return {
                "most_used": most_used["name"] if most_used else "",
                "categories": [
                    {"name": row["name"], "count": row["count"]}
                    for row in all_categories
                ],
            }
        except Exception as e:
            raise Exception(f"Error getting category stats: {e}")
