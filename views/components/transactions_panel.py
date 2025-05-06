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

        # Cabeçalho
        title = ttk.Label(inner_frame,
                        text="Últimas transações",
                        style="Title.TLabel")
        title.pack(pady=(0, 20), anchor="w")
        header = tk.Frame(inner_frame, bg=self.color_palette["white"])
        header.pack(fill="x", pady=(0, 15))
        
        ttk.Label(header,
                text="Tipo de transação",
                style="TLabel").pack(side="left", padx=5)
        ttk.Label(header, 
                text="Data",
                style="TLabel").pack(side="left", padx=5)
        ttk.Label(header, 
                text="Valor",
                style="TLabel").pack(side="right", padx=5)
        ttk.Label(header, 
                text="Descrição",
                style="TLabel").pack(side="left", padx=5, expand=True)
        

        # Linha separadora
        ttk.Separator(inner_frame, orient="horizontal").pack(fill="x", pady=5)

        # Lista de transações (exemplo)
        transactions = [
            {"type":"Receita","date": "10/05", "description": "Salário", "amount": "R$ 800,00"},
            {"type":"Receita","date": "11/05", "description": "Supermercado", "amount": "R$ 200,00"},
            {"type":"Despesa","date": "12/05", "description": "Transporte", "amount": "R$ 50,00"},
            {"type":"Despesa","date": "13/05", "description": "Lazer", "amount": "R$ 100,00"},
        ]

        for transaction in transactions:
            item = tk.Frame(inner_frame, bg=self.color_palette["white"])
            item.pack(fill="x", pady=5)

            ttk.Label(item, 
                    text=transaction["type"],
                    style="TLabel").pack(side="left", padx=5)
            ttk.Label(item, 
                    text=transaction["date"],
                    style="TLabel").pack(side="left", padx=5)
            
            ttk.Label(item, 
                    text=transaction["description"],
                    style="TLabel").pack(side="left", padx=5, expand=True)
            
            ttk.Label(item, 
                    text=transaction["amount"],
                    style="TLabel").pack(side="right", padx=5)