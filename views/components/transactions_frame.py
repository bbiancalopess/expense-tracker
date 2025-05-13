import tkinter as tk
from tkinter import ttk

class TransactionsFrame(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"], padx=10, pady=10)
        self.color_palette = color_palette
        self.create_widgets()

    def create_widgets(self):
        # Frame interno
        inner_frame = tk.Frame(self, bg=self.color_palette["white"], padx=20, pady=20)
        inner_frame.pack(expand=True, fill="both")

        # Título
        title = ttk.Label(inner_frame, 
                        text="Transações",
                        style="TLabel")
        title.pack(pady=(0, 10))

        # Lista de transações
        transactions_list = tk.Frame(inner_frame, bg=self.color_palette["white"])
        transactions_list.pack(fill="x")

        # Exemplo de transações
        tk.Label(transactions_list, 
               text="R$800,00 - Salário",
               bg=self.color_palette["white"],
               font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        
        tk.Label(transactions_list, 
               text="R$200,00 - Alimentação",
               bg=self.color_palette["white"],
               font=("Segoe UI", 10)).pack(anchor="w", pady=2)

        # Checkboxes (simulando tarefas)
        tk.Checkbutton(inner_frame, 
                     text="", 
                     bg=self.color_palette["white"]).pack(anchor="w", pady=5)
        tk.Checkbutton(inner_frame, 
                     text="", 
                     bg=self.color_palette["white"]).pack(anchor="w", pady=5)