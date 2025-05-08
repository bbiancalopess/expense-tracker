from typing import Optional
from src.models.category import Category
from src.database.db_manager import DatabaseManager


class CategoryRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_all(self) -> list[Category]:
        try:
            query = "SELECT * FROM categories;"
            results = self.db.select(query)
            if not results:
                return []

            return [Category(id=row["id"], name=row["name"]) for row in results]
        except Exception as e:
            print(f"Error getting all categories: {e}")
            return []

    def get_by_id(self, category_id: int) -> Optional[Category]:
        try:
            query = "SELECT * FROM categories WHERE id = ?;"
            result = self.db.select_one(query, (category_id,))
            if not result:
                return None

            return Category(id=result["id"], name=result["name"])
        except Exception as e:
            print(f"Error getting category by ID {category_id}: {e}")
            return None

    def save(self, category: Category) -> int:
        try:
            data = category.to_dict()

            if not data:
                return None

            if category._id:
                query = """
                    UPDATE categories SET
                    name = ?
                    WHERE id = ?
                """
                params = (
                    data["name"],
                    data["id"],
                )
                rows_affected = self.db.update(query, params)
                return category._id if rows_affected > 0 else None
            else:
                query = """
                    INSERT INTO categories
                    (name)
                    VALUES (?)
                """
                params = (data["name"],)
                return self.db.insert(query, params)
        except Exception as e:
            print(f"Error saving category: {e}")
            return None

    def delete(self, category_id: int) -> bool:
        try:
            query = "DELETE FROM categories WHERE id = ?;"
            return self.db.delete(query, (category_id,)) > 0
        except Exception as e:
            print(f"Error deleting category {category_id}: {e}")
            return False
