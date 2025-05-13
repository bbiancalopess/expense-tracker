import tkinter as tk
from tkinter import ttk

class WalletWindow(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"])
        self.color_palette = color_palette

        # Atributos de dados (futuramente vindos do banco)
        self.saldo = 0.0
        self.total_receitas = 0.0
        self.total_despesas = 0.0
        self.contas = []
        self.cartoes = []

        self.load_data_from_db()  # Aqui carregaremos os dados reais
        self.create_widgets()

    def load_data_from_db(self):
        """
        Substitua este método com a lógica real de conexão e busca dos dados no banco.
        """
        # Simulação de dados (substitua com SELECTs reais)
        self.saldo = 1800.00
        self.total_receitas = 3000.00
        self.total_despesas = 1200.00

        self.contas = [
            ("Inter", 500.00),
            ("Nubank", 500.00),
            ("C6", 800.00),
        ]

        self.cartoes = [
            ("Inter crédito", "Fecha em 01/mar", 1200.00),
        ]

    def create_widgets(self):
        content = tk.Frame(self, bg=self.color_palette["light_gray"])
        content.pack(side="left", fill="both", expand=True)

        # Saldo
        saldo_frame = tk.Frame(content, bg=self.color_palette["white"], padx=20, pady=10)
        saldo_frame.pack(fill="x", pady=(20, 10), padx=20)

        ttk.Label(saldo_frame, text="Saldo em conta", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(saldo_frame, text=f"R$ {self.saldo:,.2f}", style="TLabel").grid(row=1, column=0, sticky="w", pady=(5, 0))

        receitas_despesas = tk.Frame(saldo_frame, bg=self.color_palette["white"])
        receitas_despesas.grid(row=0, column=1, rowspan=2, sticky="e", padx=10)

        ttk.Label(receitas_despesas, text="Receitas", style="TLabel").grid(row=0, column=0, sticky="e")
        ttk.Label(receitas_despesas, text=f"R$ {self.total_receitas:,.2f}", style="TLabel").grid(row=1, column=0, sticky="e")

        ttk.Label(receitas_despesas, text="Despesas", style="TLabel").grid(row=0, column=1, sticky="e", padx=(20, 0))
        ttk.Label(receitas_despesas, text=f"R$ {self.total_despesas:,.2f}", style="TLabel").grid(row=1, column=1, sticky="e", padx=(20, 0))

        # Contas
        contas_frame = tk.Frame(content, bg=self.color_palette["white"], padx=20, pady=10)
        contas_frame.pack(fill="x", pady=(10, 5), padx=20)

        ttk.Label(contas_frame, text="Contas", style="Title.TLabel").pack(anchor="w")
        ttk.Button(contas_frame, text="Adicionar conta", style="TButton").pack(anchor="e", pady=5)

        for banco, valor in self.contas:
            box = tk.Frame(contas_frame, bg=self.color_palette["light_gray"], padx=10, pady=5)
            box.pack(fill="x", pady=5)
            ttk.Label(box, text=banco, style="TLabel").pack(anchor="w")
            ttk.Label(box, text=f"R$ {valor:,.2f}", style="TLabel").pack(anchor="w")

        total_contas = sum(valor for _, valor in self.contas)
        ttk.Label(contas_frame, text=f"Total R$ {total_contas:,.2f}", style="TLabel").pack(anchor="e", pady=5)

        # Cartões
        cartoes_frame = tk.Frame(content, bg=self.color_palette["white"], padx=20, pady=10)
        cartoes_frame.pack(fill="x", pady=(5, 20), padx=20)

        ttk.Label(cartoes_frame, text="Cartões de crédito", style="Title.TLabel").pack(anchor="w")

        for nome, vencimento, valor in self.cartoes:
            box = tk.Frame(cartoes_frame, bg=self.color_palette["light_gray"], padx=10, pady=5)
            box.pack(fill="x", pady=5)
            ttk.Label(box, text=nome, style="TLabel").pack(anchor="w")
            ttk.Label(box, text=vencimento, style="TLabel").pack(anchor="w")
            ttk.Label(box, text=f"R$ {valor:,.2f}", style="TLabel").pack(anchor="w")

        total_cartoes = sum(valor for _, _, valor in self.cartoes)
        ttk.Label(cartoes_frame, text=f"Total R$ {total_cartoes:,.2f}", style="TLabel").pack(anchor="e", pady=5)
