import pytest
import sqlite3
from src.database.db_manager import DatabaseManager
from src.repositories.payment_method_repository import PaymentMethodRepository
from src.services.payment_method_service import PaymentMethodService
from src.repositories.category_repository import CategoryRepository
from src.services.category_service import CategoryService
from src.repositories.transaction_repository import TransactionRepository
from src.services.transaction_service import TransactionService
from src.models.category import Category
from src.models.payment_method.credit import Credit


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


@pytest.fixture
def transaction_test_db():
    # Configuração do banco de teste
    db = DatabaseManager("src/database/expense-tracker-test.db")

    # Cria a tabela (se não existir)
    conn = sqlite3.connect("src/database/expense-tracker-test.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount FLOAT NOT NULL,
            description TEXT,
            date TIMESTAMP NOT NULL,
            type TEXT CHECK(type IN ('INCOME', 'EXPENSE')) NOT NULL,
            current_installment INTEGER DEFAULT 1,
            total_installments INTEGER DEFAULT 1,
            category_id INTEGER,
            payment_method_id INTEGER,
            FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id) ON DELETE SET NULL
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        )
    """
    )
    # Limpa dados anteriores
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()

    yield db  # Entrega o db para o teste

    # (Opcional) Limpeza após o teste
    conn = sqlite3.connect("src/database/expense-tracker-test.db")
    conn.cursor().execute("DELETE FROM transactions")
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


# fixtures for transaction
@pytest.fixture
def transaction_repo(transaction_test_db):
    return TransactionRepository(transaction_test_db)


@pytest.fixture
def transaction_service(transaction_repo):
    return TransactionService(transaction_repo)


@pytest.fixture
def sample_payment_method(payment_service):
    credit = Credit(id=None, name="Cartão Teste", balance=1000, credit_limit=5000)
    return payment_service.add_payment_method(credit)


@pytest.fixture
def sample_category(category_service):
    category = Category(id=None, name="Alimentação")
    return category_service.add_category(category)
