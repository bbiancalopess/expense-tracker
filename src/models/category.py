from typing import Optional


class Category:
    def __init__(self, id: Optional[int] = None, name: str = ""):
        """
        Initialize a Category with optional id and name

        Args:
            id: Unique identifier for the category (optional)
            name: Name of the category (defaults to empty string)
        """
        self._id = id
        self.name = name

    def to_dict(self) -> dict[str, any]:
        """Convert category to dictionary representation"""
        return {"id": self._id, "name": self._name}

    @property
    def id(self) -> Optional[int]:
        """Get category id"""
        return self._id

    @id.setter
    def id(self, value: Optional[int]) -> None:
        """Set category id with validation"""
        if value is not None and value < 0:
            raise ValueError("ID must be positive or None")
        self._id = value

    @property
    def name(self) -> str:
        """Get category name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set category name with validation"""
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        self._name = value.strip()

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Category":
        """Create category instance from dictionary"""
        return cls(id=data.get("id"), name=data["name"])
