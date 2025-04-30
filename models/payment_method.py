from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process_payment(self, amount: float):
        pass

    def __str__(self):
        return self.name

class CreditCard(PaymentMethod):
    def __init__(self, name: str, card_number: str, expiration_date: str):
        super().__init__(name)
        self.card_number = card_number
        self.expiration_date = expiration_date

    def process_payment(self, amount: float):
        # Logic to process credit card payment
        print(f"Processing credit card payment of {amount} using card {self.card_number}.")

class Cash(PaymentMethod):
    def __init__(self):
        super().__init__("Dinheiro")

    def process_payment(self, amount: float):
        print(f"Pagamento de R${amount:.2f} realizado em Dinheiro.")

class DebitCard(PaymentMethod):
    def __init__(self, name: str, card_number: str):
        super().__init__(name)
        self.card_number = card_number

    def process_payment(self, amount: float):
        # Logic to process debit card payment
        print(f"Processing debit card payment of {amount} using card {self.card_number}.")