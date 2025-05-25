from src.repositories.payment_method_repository import PaymentMethodRepository
from src.models.payment_method.payment_method import PaymentMethod
from typing import Optional


class PaymentMethodService:
    """
    Serviço para operações relacionadas a métodos de pagamento.
    Gerencia operações como adição, atualização e processamento de pagamentos.
    """

    def __init__(self, repository: PaymentMethodRepository):
        """
        Inicializa o serviço com o repositório de métodos de pagamento.

        Args:
            repository: Instância do PaymentMethodRepository
        """
        self.repo = repository

    def add_payment_method(self, payment: PaymentMethod) -> Optional[PaymentMethod]:
        """
        Adiciona um novo método de pagamento ao sistema.

        Args:
            payment: Objeto PaymentMethod a ser adicionado

        Returns:
            PaymentMethod: O método com ID atualizado em caso de sucesso
            None: Em caso de falha
        """
        if not isinstance(payment, PaymentMethod):
            return None

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
        """
        Recupera todos os métodos de pagamento cadastrados.

        Returns:
            List[PaymentMethod]: Lista de métodos ou lista vazia se nenhum encontrado
        """
        try:
            return self.repo.get_all()
        except Exception as e:
            print(f"Error getting all payment methods: {e}")
            return []

    def get_payment_by_id(self, payment_id: int) -> Optional[PaymentMethod]:
        """
        Busca um método de pagamento pelo seu ID.

        Args:
            payment_id: ID do método a ser buscado

        Returns:
            PaymentMethod: O método encontrado
            None: Se não encontrado ou ID inválido
        """
        if not isinstance(payment_id, int) or payment_id <= 0:
            return None

        try:
            return self.repo.get_by_id(payment_id)
        except Exception as e:
            print(f"Error getting payment method by ID {payment_id}: {e}")
            return None

    def update_payment(self, payment: PaymentMethod) -> bool:
        """
        Atualiza os dados de um método de pagamento existente.

        Args:
            payment: Objeto PaymentMethod com dados atualizados

        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        if not isinstance(payment, PaymentMethod) or not payment.id:
            return False

        try:
            return self.repo.save(payment) is not None
        except Exception as e:
            print(f"Error updating payment method {payment.id}: {e}")
            return False

    def delete_payment(self, payment_id: int) -> bool:
        """
        Remove um método de pagamento do sistema.

        Args:
            payment_id: ID do método a ser removido

        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        if not isinstance(payment_id, int) or payment_id <= 0:
            return False

        try:
            return self.repo.delete(payment_id)
        except Exception as e:
            print(f"Error deleting payment method {payment_id}: {e}")
            return False

    def process_payment(self, payment_id: int, amount: float) -> bool:
        """
        Processa um pagamento usando um método específico.

        Args:
            payment_id: ID do método de pagamento a ser usado
            amount: Valor do pagamento

        Returns:
            bool: True se o pagamento foi processado com sucesso
        """
        if not isinstance(payment_id, int) or payment_id <= 0:
            return False
        if not isinstance(amount, (int, float)) or amount <= 0:
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
            except Exception as e:
                print(f"Error processing payment: {e}")
                return False
        except Exception as e:
            print(f"Error in payment processing workflow: {e}")
            return False
