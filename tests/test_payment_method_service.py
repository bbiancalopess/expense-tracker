from src.models.payment_method.credit import Credit
from src.models.payment_method.debit import Debit


def test_full_payment_service_workflow(payment_service):
    """Full integration test for all service operation"""

    # 1. Test add_payment_method (CREDIT)
    credit_payment = Credit(
        id=None,
        name="Cartão Inter",
        balance=0,
        credit_limit=5000,
        closing_day=10,
        due_day=20,
    )
    credit_id = payment_service.add_payment_method(credit_payment).id
    assert credit_id is not None

    # 2. Test add_payment_method (DEBIT)
    debit_payment = Debit(
        id=None,
        name="Cartão Débito",
        balance=1000,
    )
    debit_id = payment_service.add_payment_method(debit_payment).id
    assert debit_id is not None

    # 3. Test get_all_payments
    payments = payment_service.get_all_payment_methods()
    assert len(payments) == 2
    assert any(p.name == "Cartão Inter" for p in payments)

    # 4. Test get_payment_by_id
    inter = payment_service.get_payment_method_by_id(credit_id)
    assert inter.credit_limit == 5000

    # 5. Test process_payment (credit)
    assert payment_service.process_payment(credit_id, 100, True) is True
    updated_credit = payment_service.get_payment_method_by_id(credit_id)
    assert updated_credit.balance == 100

    # 6. Test process_payment (debit)
    assert payment_service.process_payment(debit_id, 200, True) is True
    updated_debit = payment_service.get_payment_method_by_id(debit_id)
    assert updated_debit.balance == 800

    # 7. Test process_payment with invalid value
    assert payment_service.process_payment(credit_id, -50, True) is False

    # 8. Test update_payment
    inter.name = "Inter Black"
    assert payment_service.update_payment_method(inter) is True
    assert payment_service.get_payment_method_by_id(credit_id).name == "Inter Black"

    # 9. Test delete_payment
    assert payment_service.delete_payment_method(debit_id) is True
    assert len(payment_service.get_all_payment_methods()) == 1
