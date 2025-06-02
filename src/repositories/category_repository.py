from typing import Optional
from src.models.category import Category
from src.database.db_manager import DatabaseManager


class CategoryRepository:
    """
    Repositório para operações CRUD de categorias no banco de dados.
    Responsável por mediar a comunicação entre os objetos Category e o banco.
    """

    def __init__(self):
        """
        Inicializa o repositório com uma instância do gerenciador de banco de dados.

        Args:
            db: Gerenciador de conexão com o banco de dados
        """
        self.db = DatabaseManager()

    def get_all(self) -> list[Category]:
        """
        Recupera todas as categorias do banco de dados.

        Returns:
            Lista de objetos Category ou lista vazia se nenhuma encontrada
        """
        try:
            query = "SELECT id, name FROM categories ORDER BY name;"
            results = self.db.select(query)
            return (
                [Category(id=row["id"], name=row["name"]) for row in results]
                if results
                else []
            )
        except Exception as e:
            raise Exception(f"Error getting all categories: {str(e)}")

    def get_by_id(self, category_id: int) -> Optional[Category]:
        """
        Busca uma categoria pelo seu ID.

        Args:
            category_id: ID da categoria a ser buscada

        Returns:
            Objeto Category se encontrado, None caso contrário
        """
        try:
            query = "SELECT id, name FROM categories WHERE id = ?;"
            result = self.db.select_one(query, (category_id,))
            return Category(**result) if result else None
        except Exception as e:
            Exception(f"Error getting category by ID: {str(e)}")

    def save(self, category: Category) -> int:
        """
        Salva uma categoria no banco de dados (insere ou atualiza).

        Args:
            category: Objeto Category a ser persistido

        Returns:
            ID da categoria salva ou None em caso de falha

        Raises:
            ValueError: Se o objeto Category for inválido
        """
        if not isinstance(category, Category):
            raise ValueError("Invalid category object")

        try:
            data = category.to_dict()

            if category.id:
                # Atualização
                query = "UPDATE categories SET name = ? WHERE id = ?;"
                params = (data["name"], data["id"])
                self.db.update(query, params)
                return category.id
            else:
                # Inserção
                query = "INSERT INTO categories (name) VALUES (?);"
                params = (data["name"],)
                return self.db.insert(query, params)
        except Exception as e:
            raise Exception(f"Error saving category: {str(e)}")

    def delete(self, category_id: int) -> bool:
        """
        Remove uma categoria do banco de dados.

        Args:
            category_id: ID da categoria a ser removida

        Returns:
            True se a categoria foi removida, False caso contrário
        """
        try:
            query = "DELETE FROM categories WHERE id = ?;"
            return self.db.delete(query, (category_id,)) > 0
        except Exception as e:
            raise Exception(f"Error deleting category {category_id}: {e}")
