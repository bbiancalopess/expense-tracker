import sqlite3
from typing import Optional


class DatabaseManager:
    def __init__(self, db_file="src/database/expense-tracker-dev.db"):
        self._db_file = db_file

    def __get_connection(self):
        """Returns a database connection"""
        conn = sqlite3.connect(self._db_file)
        conn.execute("PRAGMA foreign_keys = ON;")
        # Configure to return rows as dicts
        conn.row_factory = sqlite3.Row
        return conn

    def __get_columns(self, cursor: sqlite3.Cursor) -> list[str]:
        """Returns the cursor's columns names"""
        return (
            [column[0] for column in cursor.description] if cursor.description else []
        )

    def insert(self, query: str, params: tuple) -> int | None:
        """Executes an insertion e returns the generated id"""
        try:
            with self.__get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as err:
            print(f"[INSERT ERROR] {err}")
            return None

    def select(self, query: str, params: tuple = ()) -> list[any]:
        """Executes a search and returns its results"""
        try:
            with self.__get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                columns = self.__get_columns(cursor=cursor)
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.Error as err:
            print(f"[SELECT ERROR] {err}")
            return []

    def select_one(self, query: str, params: tuple = ()) -> Optional[dict[str, any]]:
        """Executes a search and retruns only one result"""
        try:
            with self.__get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                columns = self.__get_columns(cursor)
                row = cursor.fetchone()
                return dict(zip(columns, row)) if row else None
        except sqlite3.Error as err:
            print(f"[SELECT ERROR] {err}")
            return None

    def update(self, query: str, params: tuple) -> int:
        """Executes an update and returns the affected rows number"""
        try:
            with self.__get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as err:
            print(f"[UPDATE ERROR] {err}")
            return 0

    def delete(self, query: str, params: tuple) -> int:
        """Executes an exclusion and returns the affected rows number"""
        try:
            with self.__get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except sqlite3.Error as err:
            print(f"[DELETE ERROR] {err}")
            return 0

    def execute_script(self, script: str) -> bool:
        """Executes a SQL script with multiple commands"""
        try:
            with self.__get_connection() as conn:
                conn.executescript(script)
                conn.commit()
                return True
        except sqlite3.Error as err:
            print(f"[SCRIPT ERROR] {err}")
            return False
