from src.models.payment_method.credit import Credit
from src.models.payment_method.debit import Debit


def test_full_payment_service_workflow(service):
    """Full integration test for all service operation"""

    # 1. Test add_payment_method (CREDIT)
    credit_payment = Credit(
        id=None,
        name="Cartão Inter",
        balance=0,
        credit_limit=5000,
        closing_date=10,
        due_date=20,
    )
    credit_id = service.add_payment_method(credit_payment).id
    assert credit_id is not None

    # 2. Test add_payment_method (DEBIT)
    debit_payment = Debit(
        id=None,
        name="Cartão Débito",
        balance=1000,
    )
    debit_id = service.add_payment_method(debit_payment).id
    assert debit_id is not None

    # 3. Test get_all_payments
    payments = service.get_all_payments()
    assert len(payments) == 2
    assert any(p.name == "Cartão Inter" for p in payments)

    # 4. Test get_payment_by_id
    inter = service.get_payment_by_id(credit_id)
    assert inter.credit_limit == 5000

    # 5. Test process_payment (credit)
    assert service.process_payment(credit_id, 100) is True
    updated_credit = service.get_payment_by_id(credit_id)
    assert updated_credit.balance == 100

    # 6. Test process_payment (debit)
    assert service.process_payment(debit_id, 200) is True
    updated_debit = service.get_payment_by_id(debit_id)
    assert updated_debit.balance == 800

    # 7. Test process_payment with invalid value
    assert service.process_payment(credit_id, -50) is False

    # 8. Test update_payment
    inter.name = "Inter Black"
    assert service.update_payment(inter) is True
    assert service.get_payment_by_id(credit_id).name == "Inter Black"

    # 9. Test delete_payment
    assert service.delete_payment(debit_id) is True
    assert len(service.get_all_payments()) == 1
