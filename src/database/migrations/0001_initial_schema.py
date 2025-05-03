def up():
    """Creates the initial database schema"""
    return """
    -- Criação da tabela de métodos de pagamento
    CREATE TABLE payment_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('credito', 'debito', 'dinheiro')) NOT NULL,
        balance FLOAT DEFAULT 0.0,
        credit_limit FLOAT DEFAULT 0.0,
        closing_date DATE,
        due_date DATE
    );

    -- Criação da tabela de categorias
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    -- Criação da tabela de transações
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount FLOAT NOT NULL,
        description TEXT,
        date TIMESTAMP NOT NULL,
        type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
        current_installment INTEGER DEFAULT 1,
        installment_amount INTEGER DEFAULT 1,
        category_id INTEGER,
        payment_method_id INTEGER,
        FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id) ON DELETE SET NULL
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
    );

    """


def down():
    """Removes all the initial schema"""
    return """
        DROP TABLE IF EXISTS transactions;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS payment_methods;
    """
