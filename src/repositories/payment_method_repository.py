from typing import Optional
from src.database.db_manager import DatabaseManager
from src.models.payment_method.payment_method import PaymentMethod
from src.models.payment_method.credit import Credit
from src.models.payment_method.debit import Debit
from src.models.payment_method.payment_type import PaymentType


class PaymentMethodRepository:
    """
    Repositório para operações CRUD de métodos de pagamento.
    Lida com os tipos específicos (Credit e Debit) de forma transparente.
    """
    
    def __init__(self, db: DatabaseManager):
        self.db = db

    def __create_payment_from_dict(self, data: dict) -> Optional[PaymentMethod]:
        """
        Factory method interno para criar instâncias específicas de PaymentMethod.
        
        Args:
            data: Dicionário com os dados do banco
            
        Returns:
            Instância de Credit, Debit ou None se inválido
        """
        if not data or "type" not in data:
            return None

        try:
            if data["type"] == PaymentType.CREDIT:
                return Credit.from_dict(data)
            elif data["type"] == PaymentType.DEBIT:
                return Debit.from_dict(data)
            return None
        except Exception as e:
            raise Exception(f"Error creating payment from dict: {str(e)}")

    def get_all(self) -> list[PaymentMethod]:
        """
        Recupera todos os métodos de pagamento do banco.
        
        Returns:
            Lista de PaymentMethod (Credit ou Debit) ou lista vazia
        """
        try:
            query = """
                SELECT id, name, balance, type, 
                       credit_limit, closing_day, due_day 
                FROM payment_methods;
            """
            results = self.db.select(query)
            return [self.__create_payment_from_dict(row) for row in results] if results else []
        except Exception as e:
            raise Exception(f"Error getting all payment methods: {e}")

    def get_by_id(self, payment_id: int) -> Optional[PaymentMethod]:
        """
        Busca um método de pagamento pelo ID.
        
        Args:
            payment_id: ID do método de pagamento
            
        Returns:
            Instância de PaymentMethod ou None se não encontrado
        """
        try:
            query = """
                SELECT id, name, balance, type, 
                       credit_limit, closing_day, due_day 
                FROM payment_methods 
                WHERE id = ?;
            """
            result = self.db.select_one(query, (payment_id,))
            return self.__create_payment_from_dict(result) if result else None
        except Exception as e:
            raise Exception(f"Error getting payment method by ID {payment_id}: {e}")

    def save(self, payment: PaymentMethod) -> int:
        """
        Salva um método de pagamento no banco (insere ou atualiza).
        
        Args:
            payment: Instância de Credit ou Debit
            
        Returns:
            ID do método salvo ou None em caso de falha
            
        Raises:
            ValueError: Se o objeto payment for inválido
        """
        if not isinstance(payment, PaymentMethod):
            raise ValueError("Invalid payment method object")

        try:
            data = payment.to_dict()
            
            if payment.id:
                # Atualização
                query = """
                    UPDATE payment_methods SET
                    name = ?, balance = ?, type = ?,
                    credit_limit = ?, closing_day = ?, due_day = ?
                    WHERE id = ?;
                """
                params = (
                    data["name"],
                    data["balance"],
                    data["type"],
                    data.get("credit_limit"),
                    data.get("closing_day"),
                    data.get("due_day"),
                    data["id"]
                )
                self.db.update(query, params)
                return payment.id
            else:
                # Inserção
                query = """
                    INSERT INTO payment_methods 
                    (name, balance, type, credit_limit, closing_day, due_day)
                    VALUES (?, ?, ?, ?, ?, ?);
                """
                params = (
                    data["name"],
                    data["balance"],
                    data["type"],
                    data.get("credit_limit"),
                    data.get("closing_day"),
                    data.get("due_day")
                )
                return self.db.insert(query, params)
        except Exception as e:
            raise Exception(f"Error saving payment method: {e}")

    def delete(self, payment_id: int) -> bool:
        """
        Remove um método de pagamento do banco.
        
        Args:
            payment_id: ID do método a ser removido
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        try:
            query = "DELETE FROM payment_methods WHERE id = ?;"
            return self.db.delete(query, (payment_id,)) > 0
        except Exception as e:
            raise Exception(f"Error deleting payment method {payment_id}: {e}")
