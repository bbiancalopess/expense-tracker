from src.repositories.category_repository import CategoryRepository
from src.models.category import Category
from typing import Optional


class CategoryService:
    """
    Serviço para operações relacionadas a categorias.
    Atua como uma camada intermediária entre os controllers e o repositório,
    podendo incluir lógica de negócio adicional.
    """

    def __init__(self, repository: CategoryRepository):
        """
        Inicializa o serviço com o repositório de categorias.

        Args:
            repository: Instância do CategoryRepository para operações de persistência
        """
        self.repo = repository

    def add_category(self, category: Category) -> Optional[Category]:
        """
        Adiciona uma nova categoria ao sistema.

        Args:
            category: Objeto Category a ser adicionado

        Returns:
            Category: A categoria com ID atualizado em caso de sucesso
            None: Em caso de falha
        """
        if not isinstance(category, Category):
            return None

        try:
            category_id = self.repo.save(category)
            if category_id:
                category._id = category_id
                return category
            return None
        except Exception as e:
            print(f"Error adding category: {e}")
            return None

    def get_all_categories(self) -> list[Category]:
        """
        Recupera todas as categorias cadastradas.

        Returns:
            List[Category]: Lista de categorias ou lista vazia se nenhuma encontrada
        """
        try:
            return self.repo.get_all()
        except Exception as e:
            print(f"Error getting all categories: {e}")
            return []

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """
        Busca uma categoria pelo seu ID.

        Args:
            category_id: ID da categoria a ser buscada

        Returns:
            Category: A categoria encontrada
            None: Se não encontrada ou ID inválido
        """
        if not isinstance(category_id, int) or category_id <= 0:
            return None

        try:
            return self.repo.get_by_id(category_id)
        except Exception as e:
            print(f"Error getting category by ID {category_id}: {e}")
            return None

    def update_category(self, category: Category) -> bool:
        """
        Atualiza os dados de uma categoria existente.

        Args:
            category: Objeto Category com dados atualizados

        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        if not isinstance(category, Category) or not category.id:
            return False

        try:
            return self.repo.save(category) is not None
        except Exception as e:
            print(f"Error updating category {category.id}: {e}")
            return False

    def delete_category(self, category_id: int) -> bool:
        """
        Remove uma categoria do sistema.

        Args:
            category_id: ID da categoria a ser removida

        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        if not isinstance(category_id, int) or category_id <= 0:
            return False

        try:
            return self.repo.delete(category_id)
        except Exception as e:
            print(f"Error deleting category {category_id}: {e}")
            return False
