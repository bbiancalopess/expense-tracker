class Wallet:
    def __init__(self):
        self.payment_methods = []

    def add_payment_method(self, payment_method):
        self.payment_methods.append(payment_method)

    def remove_payment_method(self, payment_method):
        self.payment_methods.remove(payment_method)

    def get_total_balance(self):
        return sum(method.get_balance() for method in self.payment_methods)

    def get_payment_method(self, name):
        for method in self.payment_methods:
            if method.name == name:
                return method
        return None
