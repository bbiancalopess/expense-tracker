from src.repositories.category_repository import CategoryRepository
from src.models.category import Category
from typing import Optional


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repo = repository

    def add_category(self, category: Category) -> Category:
        try:
            category_id = self.repo.save(category)
            if category_id:
                category.id = category_id
                return category
            return None
        except Exception as e:
            print(f"Error adding category: {e}")
            return None

    def get_all_categories(self) -> list[Category]:
        try:
            return self.repo.get_all()
        except Exception as e:
            print(f"Error getting all categories service: {e}")
            return []

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        if category_id <= 0:
            return None

        try:
            return self.repo.get_by_id(category_id)
        except Exception as e:
            print(f"Error getting category by ID {category_id}: {e}")
            return None

    def update_category(self, category: Category) -> bool:
        try:
            return self.repo.save(category) is not None
        except Exception as e:
            print(f"Error updating category {category.id}: {e}")
            return False

    def delete_category(self, category_id: int) -> bool:
        if category_id <= 0:
            return False

        try:
            return self.repo.delete(category_id)
        except Exception as e:
            print(f"Error deleting category {category_id}: {e}")
            return False
