import importlib
from pathlib import Path
from typing import Optional
import inspect
from src.database.db_manager import DatabaseManager


class MigrationManager:
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self._db = db_manager or DatabaseManager()
        self._migrations_dir = Path(__file__).parent / "migrations"
        self.__ensure_migrations_table()

    def __ensure_migrations_table(self) -> None:
        "Creates migrations table if it doesn't exists"
        self._db.execute_script(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                pplied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

    def __get_applied_migrations(self) -> list[str]:
        """Returns the migrations already applied"""
        results = self._db.select("SELECT name FROM migrations ORDER BY id")
        return [row[0] for row in results]

    def __get_pending_migrations(self) -> list[str]:
        """Returns pending migrations"""
        applied = set(self.__get_applied_migrations())
        all_migrations = sorted(
            f.stem
            for f in self._migrations_dir.glob("*.py")
            if not f.name.startswith("__") and f.name != "__init__.py"
        )
        return [m for m in all_migrations if m not in applied]

    def __load_migration_module(self, migration_name: str):
        """Loads the migration module"""
        module_name = f"database.migrations.{migration_name}"
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            print(f"Error loading migration {migration_name}: {e}")
            raise

    def __execute_migration_function(self, func, migration_name: str) -> bool:
        params = inspect.signature(func).parameters
        try:
            if "db" in params:
                func(db=self._db)
            else:
                result = func()
                if isinstance(result, str):
                    self._db.execute_script(result)
                elif isinstance(result, list):
                    for cmd in result:
                        self._db.execute_script(cmd)
            return True
        except Exception as err:
            print(f"Failed to apply migration {migration_name}: {err}")
            return False

    def __apply_migration(self, migration_name: str) -> bool:
        """Applies an especific migration"""
        module = self.__load_migration_module(migration_name)

        if not hasattr(module, "up"):
            print(f"Migration {migration_name} doens't have an up function")
            return False

        success = self.__execute_migration_function(module.up, migration_name)

        if success:
            self._db.insert(
                "INSERT INTO migrations (name) VALUES (?)", (migration_name,)
            )
            print(f"✅ Migration applied successfully: {migration_name}")
        else:
            print(f"❌ Failed to apply migration {migration_name}")

        return success

    def apply_all_pending(self) -> int:
        """Applies all pending migration"""
        pending = self.__get_pending_migrations()
        if not pending:
            print("🔹 No pending migrations")
            return 0

        print(f"🔹 Applying {len(pending)} pending migrations")
        success_count = 0

        for migration in pending:
            if self.__apply_migration(migration):
                success_count += 1
            else:
                print(f"🛑 Stopping due to error on migration: {migration}")
                break

        print(f"🔹 Total de migrations aplicadas: {success_count}/{len(pending)}")
        return success_count

    def __rollback_migration(self, migration_name: str) -> bool:
        """Reverts an especific migration"""
        module = self.__load_migration_module(migration_name)

        if not hasattr(module, "down"):
            print(f"Migration {migration_name} doens't have an down function")
            return False

        success = self.__execute_migration_function(module.down, migration_name)

        if success:
            self._db.delete("DELETE FROM migrations WHERE name = ?", (migration_name,))
            print(f"✅ Migration reverted successfully: {migration_name}")
        else:
            print(f"❌ Failed to revert migration {migration_name}")

        return success
