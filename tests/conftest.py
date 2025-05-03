import pytest
import sqlite3
from database.db_manager import DatabaseManager
from repositories.payment_method_repository import PaymentMethodRepository
from services.payment_method_service import PaymentMethodService


@pytest.fixture
def test_db():
    # Configuração do banco de teste
    db = DatabaseManager("database/expense-tracker-test.db")

    # Cria a tabela (se não existir)
    conn = sqlite3.connect("database/expense-tracker-test.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS payment_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL NOT NULL,
            type TEXT NOT NULL,
            credit_limit REAL,
            closing_date TEXT,
            due_date TEXT
        )
    """
    )
    # Limpa dados anteriores
    cursor.execute("DELETE FROM payment_methods")
    conn.commit()
    conn.close()

    yield db  # Entrega o db para o teste

    # (Opcional) Limpeza após o teste
    conn = sqlite3.connect("database/expense-tracker-test.db")
    conn.cursor().execute("DELETE FROM payment_methods")
    conn.commit()
    conn.close()


@pytest.fixture
def repo(mock_db):
    from repositories.payment_method_repository import PaymentMethodRepository

    return PaymentMethodRepository(test_db)


@pytest.fixture
def service(test_db):
    repo = PaymentMethodRepository(test_db)
    return PaymentMethodService(repo)
