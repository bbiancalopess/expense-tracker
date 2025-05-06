import pytest
from src.models.transaction.income import Income
from src.models.transaction.expense import Expense
from src.models.payment_method.credit import Credit


def test_full_transaction_workflow(
    transaction_service, sample_payment_method, sample_category
):
    """Full integration test for all service operation"""

    # 1. Test creating a new income
    income = Income(
        amount=3000, description="Salário", payment_method=sample_payment_method
    )
    saved_income = transaction_service.add_transaction(income)
    assert saved_income.id is not None
    assert saved_income.amount == 3000
    assert saved_income.payment_method.id == sample_payment_method.id

    # 2. Test creating a new expense
    expense = Expense(
        amount=150,
        description="Superercado",
        category=sample_category,
        payment_method=sample_payment_method,
        total_installments=3,
    )
    saved_expense = transaction_service.add_transaction(expense)
    assert saved_expense.id is not None
    assert saved_expense.category.id == sample_category.id

    # 3. Test get_all_transactions
    transactions = transaction_service.get_all_transactions()
    assert len(transactions) == 2
    assert isinstance(transactions[0], (Income, Expense))

    # 4. Test get_transaction_by_id
    fetched_income = transaction_service.get_transaction_by_id(saved_income.id)
    assert fetched_income.description == "Salário"

    # 5. Test update_transaction
    expense.description = "Mercado Municipal"
    assert transaction_service.update_transaction(expense) is True
    updated = transaction_service.get_transaction_by_id(expense.id)
    assert updated.description == "Mercado Municipal"

    # 6. Test delete_transaction
    assert transaction_service.delete_transaction(saved_income.id) is True
    assert len(transaction_service.get_all_transactions()) == 1
