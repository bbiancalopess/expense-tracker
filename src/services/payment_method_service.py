from src.repositories.payment_method_repository import PaymentMethodRepository
from src.models.payment_method.payment_method import PaymentMethod
from typing import Optional


class PaymentMethodService:
    def __init__(self, repository: PaymentMethodRepository):
        self.repo = repository

    def add_payment_method(self, payment: PaymentMethod) -> PaymentMethod:
        try:
            payment_id = self.repo.save(payment)
            if payment_id:
                payment._id = payment_id
                return payment
            return None
        except Exception as e:
            print(f"Error adding payment method: {e}")
            return None

    def get_all_payments(self) -> list[PaymentMethod]:
        try:
            return self.repo.get_all()
        except Exception as e:
            print(f"Error getting all payment methods service: {e}")
            return []

    def get_payment_by_id(self, payment_id: int) -> Optional[PaymentMethod]:
        if payment_id <= 0:
            return None

        try:
            return self.repo.get_by_id(payment_id)
        except Exception as e:
            print(f"Error getting payment method by ID {payment_id}: {e}")
            return None

    def update_payment(self, payment: PaymentMethod) -> bool:
        try:
            return self.repo.save(payment) is not None
        except Exception as e:
            print(f"Error updating payment method {payment._id}: {e}")
            return False

    def delete_payment(self, payment_id: int) -> bool:
        if payment_id <= 0:
            return False

        try:
            return self.repo.delete(payment_id)
        except Exception as e:
            print(f"Error deleting payment method {payment_id}: {e}")
            return False

    def process_payment(self, payment_id: int, amount: float) -> bool:
        if payment_id <= 0:
            return False
        if amount <= 0:
            return False

        try:
            payment = self.get_payment_by_id(payment_id)
            if not payment:
                return False
            try:
                success = payment.process_payment(amount)
                if success:
                    self.update_payment(payment)
                return success
            except Exception as err:
                print(f"Error processing payment: {err}")
                return False
        except Exception as err:
            print(f"Error in payment processing workflow: {err}")
            return False
