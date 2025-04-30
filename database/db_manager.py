import sqlite3


class DatabaseManager:
    def __init__(self, db_file="expense-tracker-dev.db"):
        self.db_file = db_file

    def get_connection(self):
        return sqlite3.connect(self.db_file)

    def insert(self, query, params) -> int | None:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as err:
            print(f"[INSERT ERROR] {err}")
            return None

    def select(self, query, params=()) -> list[any]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as err:
            print(f"[SELECT ERROR] {err}")
            return []

    def update(self, query, params) -> int:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as err:
            print(f"[UPDATE ERROR] {err}")
            return 0

    def delete(self, query, params) -> int:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as err:
            print(f"[DELETE ERROR] {err}")
            return 0
