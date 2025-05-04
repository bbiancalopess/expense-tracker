import pytest
import sqlite3
from src.database.db_manager import DatabaseManager
from src.repositories.payment_method_repository import PaymentMethodRepository
from src.services.payment_method_service import PaymentMethodService
from src.repositories.category_repository import CategoryRepository
from src.services.category_service import CategoryService


@pytest.fixture
def payment_test_db():
    # Configuração do banco de teste
    db = DatabaseManager("src/database/expense-tracker-test.db")

    # Cria a tabela (se não existir)
    conn = sqlite3.connect("src/database/expense-tracker-test.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS payment_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT CHECK(type IN ('CREDIT', 'DEBIT')) NOT NULL,
            balance FLOAT DEFAULT 0.0,
            credit_limit FLOAT,
            closing_day INTEGER,
            due_day INTEGER
        )
    """
    )
    # Limpa dados anteriores
    cursor.execute("DELETE FROM payment_methods")
    conn.commit()
    conn.close()

    yield db  # Entrega o db para o teste

    # (Opcional) Limpeza após o teste
    conn = sqlite3.connect("src/database/expense-tracker-test.db")
    conn.cursor().execute("DELETE FROM payment_methods")
    conn.commit()
    conn.close()


@pytest.fixture
def category_test_db():
    # Configuração do banco de teste
    db = DatabaseManager("src/database/expense-tracker-test.db")

    # Cria a tabela (se não existir)
    conn = sqlite3.connect("src/database/expense-tracker-test.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """
    )
    # Limpa dados anteriores
    cursor.execute("DELETE FROM categories")
    conn.commit()
    conn.close()

    yield db  # Entrega o db para o teste

    # (Opcional) Limpeza após o teste
    conn = sqlite3.connect("src/database/expense-tracker-test.db")
    conn.cursor().execute("DELETE FROM categories")
    conn.commit()
    conn.close()


# fixtures for payment_method
@pytest.fixture
def payment_repo(payment_test_db):
    return PaymentMethodRepository(payment_test_db)


@pytest.fixture
def payment_service(payment_repo):
    return PaymentMethodService(payment_repo)


# fixtures for category
@pytest.fixture
def category_repo(category_test_db):
    return CategoryRepository(category_test_db)


@pytest.fixture
def category_service(category_repo):
    return CategoryService(category_repo)
