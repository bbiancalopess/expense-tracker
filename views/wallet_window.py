import tkinter as tk
from tkinter import ttk
from views.add_account_window import AddAccountWindow

class WalletWindow(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.parent = parent
        
        # Atributos de dados
        self.saldo = 0.0
        self.total_receitas = 0.0
        self.total_despesas = 0.0
        self.contas = []
        self.cartoes = []

        self.load_data_from_db()
        self.create_widgets()

    def load_data_from_db(self):
        """Método para carregar dados do banco"""
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

    def open_add_account_window(self):
        if hasattr(self, '_add_window') and self._add_window.winfo_exists():
            self._add_window.lift()
            return
        
        self._add_window = AddAccountWindow(master=self.parent)
        self._add_window.grab_set()

    def create_widgets(self):
        # Frame principal que ocupa todo o espaço
        main_frame = tk.Frame(self, bg=self.color_palette["light_gray"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header com saldo e valores
        header_frame = tk.Frame(main_frame, bg=self.color_palette["white"], padx=20, pady=15)
        header_frame.pack(fill="x", pady=(0, 20))

        # Saldo total
        saldo_frame = tk.Frame(header_frame, bg=self.color_palette["white"])
        saldo_frame.pack(side="left", fill="y")

        ttk.Label(saldo_frame, text="Saldo em conta", style="Title.TLabel").pack(anchor="w")
        ttk.Label(saldo_frame, text=f"R$ {self.saldo:,.2f}", style="TLabel").pack(anchor="w", pady=(5, 0))

        # Receitas e Despesas
        values_frame = tk.Frame(header_frame, bg=self.color_palette["white"])
        values_frame.pack(side="right", fill="y")

        # Receitas
        receitas_frame = tk.Frame(values_frame, bg=self.color_palette["white"])
        receitas_frame.pack(side="left", padx=20)
        ttk.Label(receitas_frame, text="Receitas", style="TLabel").pack(anchor="e")
        ttk.Label(receitas_frame, text=f"R$ {self.total_receitas:,.2f}", style="TLabel").pack(anchor="e")

        # Despesas
        despesas_frame = tk.Frame(values_frame, bg=self.color_palette["white"])
        despesas_frame.pack(side="left", padx=20)
        ttk.Label(despesas_frame, text="Despesas", style="TLabel").pack(anchor="e")
        ttk.Label(despesas_frame, text=f"R$ {self.total_despesas:,.2f}", style="TLabel").pack(anchor="e")

        # Frame para conteúdo rolável
        canvas = tk.Canvas(main_frame, bg=self.color_palette["light_gray"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.color_palette["light_gray"])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_scrollable_frame(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)
        canvas.configure(yscrollcommand=scrollbar.set)


        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Contas
        contas_frame = tk.Frame(scrollable_frame, bg=self.color_palette["white"], padx=20, pady=15)
        contas_frame.pack(fill="both", pady=(0, 10), expand=True) 

        ttk.Label(contas_frame, text="Contas", style="Title.TLabel").pack(anchor="w")

        for banco, valor in self.contas:
            conta_item = tk.Frame(contas_frame, bg=self.color_palette["light_gray"], padx=10, pady=8)
            conta_item.pack(fill="x", pady=5, expand=True)
            ttk.Label(conta_item, text=banco, style="TLabel").pack(side="left")
            ttk.Label(conta_item, text=f"R$ {valor:,.2f}", style="TLabel").pack(side="right")

        total_contas = sum(valor for _, valor in self.contas)
        ttk.Label(contas_frame, text=f"Total R$ {total_contas:,.2f}", style="TLabel").pack(anchor="e", pady=5)

        # Botão Adicionar Conta
        add_btn = ttk.Button(scrollable_frame, text="Adicionar conta", style="TButton", command=self.open_add_account_window)
        add_btn.pack(fill="x", padx=20, pady=(0, 20)) 


        # Cartões
        cartoes_frame = tk.Frame(scrollable_frame, bg=self.color_palette["white"], padx=20, pady=15)
        cartoes_frame.pack(fill="both", expand=True) 

        ttk.Label(cartoes_frame, text="Cartões de crédito", style="Title.TLabel").pack(anchor="w")

        for nome, vencimento, valor in self.cartoes:
            cartao_item = tk.Frame(cartoes_frame, bg=self.color_palette["light_gray"], padx=10, pady=8)
            cartao_item.pack(fill="x", pady=5, expand=True)
            
            info_frame = tk.Frame(cartao_item, bg=self.color_palette["light_gray"])
            info_frame.pack(side="left", fill="x", expand=True)
            ttk.Label(info_frame, text=nome, style="TLabel").pack(anchor="w")
            ttk.Label(info_frame, text=vencimento, style="TLabel").pack(anchor="w")
            
            ttk.Label(cartao_item, text=f"R$ {valor:,.2f}", style="TLabel").pack(side="right")

        total_cartoes = sum(valor for _, _, valor in self.cartoes)
        ttk.Label(cartoes_frame, text=f"Total R$ {total_cartoes:,.2f}", style="TLabel").pack(anchor="e", pady=5)

        # Configurar scroll com mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))