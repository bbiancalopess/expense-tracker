from src.repositories.transaction_repository import TransactionRepository
from src.models.transaction.transaction import Transaction
from src.models.transaction.expense import Expense
from src.services.payment_method_service import PaymentMethodService
from src.services.category_service import CategoryService
from typing import Optional
from src.models.transaction.transaction_type import TransactionType


class TransactionService:
    """
    Serviço para operações relacionadas a transações financeiras.
    Gerencia operações como registro, atualização e exclusão de transações.
    """

    def __init__(self):
        """
        Inicializa o serviço com o repositório de transações.

        Args:
            repository: Instância do TransactionRepository
        """
        self.repo = TransactionRepository()
        self.payment_service = PaymentMethodService()
        self.category_service = CategoryService()

    def add_transaction(self, transaction: Transaction) -> Optional[Transaction]:
        """
        Adiciona uma nova transação ao sistema.

        Args:
            transaction: Objeto Transaction a ser adicionado

        Returns:
            Transaction: A transação com ID atualizado em caso de sucesso
            None: Em caso de falha ou dados inválidos
        """
        if not isinstance(transaction, Transaction):
            return None
        if isinstance(transaction, Expense):
            if transaction.category and not transaction.category.id:
                saved_category = self.category_service.add_category(
                    transaction.category
                )
                transaction.category = saved_category

            if transaction.payment_method and not transaction.payment_method.id:
                saved_payment = self.payment_service.add_payment_method(
                    transaction.payment_method
                )
                transaction.payment_method = saved_payment
        try:
            self.payment_service.process_payment(
                transaction.payment_method.id, transaction.amount,
                transaction.transaction_type == TransactionType.EXPENSE
            )
            transaction_id = self.repo.save(transaction)
            if transaction_id:
                transaction._id = transaction_id
                return transaction
            return None
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None

    def get_all_transactions(self) -> list[Transaction]:
        """
        Recupera todas as transações cadastradas.

        Returns:
            List[Transaction]: Lista de transações ou lista vazia se nenhuma encontrada
        """
        try:
            return self.repo.get_all()
        except Exception as e:
            print(f"Error getting all transactions: {e}")
            return []

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """
        Busca uma transação pelo seu ID.

        Args:
            transaction_id: ID da transação a ser buscada

        Returns:
            Transaction: A transação encontrada
            None: Se não encontrada ou ID inválido
        """
        if not isinstance(transaction_id, int) or transaction_id <= 0:
            return None

        try:
            return self.repo.get_by_id(transaction_id)
        except Exception as e:
            print(f"Error getting transaction by ID {transaction_id}: {e}")
            return None

    def update_transaction(self, transaction: Transaction) -> bool:
        """
        Atualiza os dados de uma transação existente.

        Args:
            transaction: Objeto Transaction com dados atualizados

        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        if not isinstance(transaction, Transaction) or not transaction.id:
            return False

        try:
            return self.repo.save(transaction) is not None
        except Exception as e:
            print(f"Error updating transaction {transaction.id}: {e}")
            return False

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Remove uma transação do sistema.

        Args:
            transaction_id: ID da transação a ser removida

        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        if not isinstance(transaction_id, int) or transaction_id <= 0:
            return False

        try:
            return self.repo.delete(transaction_id)
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False

    def find_current_month_totals_by_payment_method(
        self,
    ) -> dict[int, dict[str, float]]:
        """
        Retorna os totais de receitas e despesas do mês atual agrupados por método de pagamento.

        Returns:
            dict[int, dict[str, float]]:
            - Chave: ID do método de pagamento
            - Valor: Dicionário com:
                - 'income': total de receitas no mês
                - 'expense': total de despesas no mês

        Raises:
            Exception: Se ocorrer um erro ao acessar o repositório
        """
        try:
            return self.repo.get_current_month_totals_by_payment_method()
        except Exception as e:
            error_msg = f"Error getting current month totals by payment method: {e}"
            print(error_msg)
            raise Exception(error_msg) from e

    def find_total_expense_for_current_month(
        self,
    ) -> float:
        """
        Retorna o total gasto no mês.

        Returns:
            float
        Raises:
            Exception: Se ocorrer um erro ao acessar o repositório
        """
        try:
            return self.repo.get_total_expenses_for_current_month()
        except Exception as e:
            error_msg = f"Error getting total expenses for current month: {e}"
            print(error_msg)
            raise Exception(error_msg) from e

    def find_most_used_category_for_current_month(
        self,
    ) -> str:
        """
        Retorna a cateogria mais usada no mês.

        Returns:
            str
        Raises:
            Exception: Se ocorrer um erro ao acessar o repositório
        """
        try:
            return self.repo.get_most_added_category_for_current_month()
        except Exception as e:
            error_msg = f"Error getting most used category for current month: {e}"
            print(error_msg)
            raise Exception(error_msg) from e

    def count_transactions(self) -> int:
        """
        Retorna o número total de transações no mês atual

        Returns:
            int: Número de transações
        """
        try:
            return self.repo.count_month_transactions()
        except Exception as e:
            error_msg = f"Error counting transactions: {e}"
            print(error_msg)
            raise Exception(error_msg) from e

    def find_expenses_per_category_for_current_month(self) -> list[dict]:
        """
        Retorna as despesas agrupadas por categoria no mês atual

        Returns:
            List[dict]: Lista com {'name': str, 'total_expense': float}
        """
        try:
            return self.repo.get_expenses_per_category_for_current_month()
        except Exception as e:
            error_msg = f"Error getting expenses per category: {e}"
            print(error_msg)
            raise Exception(error_msg) from e

    def get_monthly_expenses(self) -> list[dict]:
        """
        Retorna os gastos mensais para os últimos 12 meses
        Returns:
            List[dict]: Lista com {'month': 'MM/YYYY', 'total': float}
        """
        try:
            return self.repo.get_monthly_expenses()
        except Exception as e:
            print(f"Error getting monthly expenses: {e}")
            return []

    def get_category_stats(self) -> dict:
        """
        Retorna estatísticas por categoria
        Returns:
            dict: {'most_used': str, 'categories': list}
        """
        try:
            return self.repo.get_category_stats()
        except Exception as e:
            print(f"Error getting category stats: {e}")
            return {"most_used": "", "categories": []}
