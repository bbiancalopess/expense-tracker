from abc import ABC, abstractmethod
from datetime import date

class Transaction(ABC):
    def __init__(self, value: float, date: date, description: str, category: str, payment_method: str, id: int = None):
        self.id = id
        self.value = value
        self.data = date
        self.description = description
        self.category = category
        self.payment_method = payment_method

    @abstractmethod
    def tipo(self):
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "date": self.date.isoformat(),
            "description": self.description,
            "category": self.category,
            "payment_method": self.payment_method,
            "type": self.type()
        }

    def __str__(self):
        return f"[{self.type()}] R${self.value:.2f} - {self.category} - {self.date} ({self.description})"

    
