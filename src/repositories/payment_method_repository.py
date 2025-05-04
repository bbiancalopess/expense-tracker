from typing import Optional
from src.database.db_manager import DatabaseManager
from src.models.payment_method.payment_method import PaymentMethod
from src.models.payment_method.credit import Credit
from src.models.payment_method.debit import Debit


class PaymentMethodRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def _create_payment_from_dict(self, data: dict) -> Optional[PaymentMethod]:
        if not data or not data.get("name") or not data.get("type"):
            return None

        try:
            payment_type = data.get("type")

            common_params = {
                "id": data.get("id"),
                "name": data.get("name"),
                "balance": data.get("balance", 0.0),
            }

            if payment_type == "CREDIT":
                return Credit(
                    **common_params,
                    credit_limit=data.get("credit_limit", 0.0),
                    closing_day=data.get("closing_day"),
                    due_day=data.get("due_day"),
                )
            elif payment_type == "DEBIT":
                return Debit(**common_params)

            return None
        except Exception as err:
            print(f"Error creating payment from dict: {err}")
            return None

    def get_all(self) -> list[PaymentMethod]:
        try:
            query = "SELECT * FROM payment_methods;"
            results = self.db.select(query)
            if not results:
                return []

            return [self._create_payment_from_dict(row) for row in results]
        except Exception as e:
            print(f"Error getting all payment methods: {e}")
            return []

    def get_by_id(self, payment_id: int) -> Optional[PaymentMethod]:
        try:
            query = "SELECT * FROM payment_methods WHERE id = ?;"
            result = self.db.select_one(query, (payment_id,))
            if not result:
                return None

            return self._create_payment_from_dict(result)
        except Exception as e:
            print(f"Error getting payment method by ID {payment_id}: {e}")
            return None

    def save(self, payment: PaymentMethod) -> int:
        try:
            data = payment.to_dict()

            if not data:
                return None

            if payment.id:
                query = """
                    UPDATE payment_methods SET
                    name = ?, balance = ?, type = ?,
                    credit_limit = ?, closing_day = ?, due_day = ?
                    WHERE id = ?
                """
                params = (
                    data["name"],
                    data["balance"],
                    data["type"],
                    data.get("credit_limit", 0),
                    data.get("closing_day"),
                    data.get("due_day"),
                    data["id"],
                )
                rows_affected = self.db.update(query, params)
                return payment.id if rows_affected > 0 else None
            else:
                query = """
                    INSERT INTO payment_methods
                    (name, balance, type, credit_limit, closing_day, due_day)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                params = (
                    data["name"],
                    data["balance"],
                    data["type"],
                    data.get("credit_limit", 0),
                    data.get("closing_day"),
                    data.get("due_day"),
                )
                return self.db.insert(query, params)
        except Exception as e:
            print(f"Error saving payment method: {e}")
            return None

    def delete(self, payment_id: int) -> bool:
        try:
            query = "DELETE FROM payment_methods WHERE id = ?;"
            return self.db.delete(query, (payment_id,)) > 0
        except Exception as e:
            print(f"Error deleting payment method {payment_id}: {e}")
            return False
