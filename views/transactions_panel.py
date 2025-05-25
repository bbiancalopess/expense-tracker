import tkinter as tk
from tkinter import ttk


class TransactionsPanel(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.create_widgets()

    def create_widgets(self):
        # Frame interno com borda
        inner_frame = tk.Frame(self, bg=self.color_palette["white"], padx=20, pady=20)
        inner_frame.pack(expand=True, fill="both")

        # Título
        title = ttk.Label(
            inner_frame,
            text="Últimas transações",
            style="Title.TLabel",
            background=self.color_palette["white"],
        )
        title.pack(pady=(0, 20), anchor="w")

        # Tabela com headers e valores
        table = tk.Frame(inner_frame, bg=self.color_palette["white"])
        table.pack(fill="x")

        # Cabeçalhos
        ttk.Label(table, text="Tipo de transação", style="TLabel").grid(
            row=0, column=0, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Data", style="TLabel").grid(
            row=0, column=1, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Categoria", style="TLabel").grid(
            row=0, column=2, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Valor", style="TLabel").grid(
            row=0, column=3, sticky="e", padx=5, pady=(0, 5)
        )

        # Lista de transações
        transactions = [
            {
                "type": "Receita",
                "date": "10/05",
                "category": "Salário",
                "amount": "R$ 800,00",
            },
            {
                "type": "Receita",
                "date": "11/05",
                "category": "Supermercado",
                "amount": "R$ 200,00",
            },
            {
                "type": "Despesa",
                "date": "12/05",
                "category": "Transporte",
                "amount": "R$ 50,00",
            },
            {
                "type": "Despesa",
                "date": "13/05",
                "category": "Lazer",
                "amount": "R$ 100,00",
            },
        ]

        for i, transaction in enumerate(transactions, start=1):
            ttk.Label(table, text=transaction["type"], style="TLabel").grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )
            ttk.Label(table, text=transaction["date"], style="TLabel").grid(
                row=i, column=1, sticky="w", padx=5, pady=2
            )
            ttk.Label(table, text=transaction["category"], style="TLabel").grid(
                row=i, column=2, sticky="w", padx=5, pady=2
            )
            ttk.Label(table, text=transaction["amount"], style="TLabel").grid(
                row=i, column=3, sticky="e", padx=5, pady=2
            )

        # Permitir que a coluna de descrição se expanda
        table.grid_columnconfigure(2, weight=1)
