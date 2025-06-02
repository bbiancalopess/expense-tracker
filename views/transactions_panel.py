import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from src.services.transaction_service import TransactionService
from src.models.transaction.transaction_type import TransactionType
from src.models.transaction.expense import Expense


class TransactionsPanel(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.transaction_service = TransactionService()
        self.canvas = None
        self.inner_frame = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.color_palette["light_gray"])
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            main_frame, bg=self.color_palette["white"], highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            main_frame, orient="vertical", command=self.canvas.yview
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=self.color_palette["white"])

        self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor="nw", tags="inner_frame"
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig("inner_frame", width=e.width),
        )

        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.canvas.itemconfig("inner_frame", width=event.width)

        self.inner_frame.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            self.canvas.itemconfig("inner_frame", width=event.width)

        self.canvas.bind("<Configure>", on_canvas_configure)

        # Cria o cabeçalho
        self.create_header()
        # Cria a lista de transações
        self.create_transaction_list()

    def create_header(self):
        """Cria o cabeçalho do painel de transações"""
        self.header_frame = tk.Frame(
            self.inner_frame, bg=self.color_palette["white"], padx=20, pady=20
        )
        self.header_frame.pack(fill="x", pady=(0, 20))

        # Título
        title = ttk.Label(
            self.header_frame,
            text="Transações",
            style="Title.TLabel",
            background=self.color_palette["white"],
        )
        title.pack(side="left", anchor="w")

        dates_frame = tk.Frame(self.header_frame, bg=self.color_palette["white"])
        dates_frame.pack(side="right", anchor="e")

    def create_transaction_list(self):
        """Cria a lista de transações"""
        # Tabela com headers e valores
        table = tk.Frame(self.inner_frame, bg=self.color_palette["white"])
        table.pack(fill="both", expand=True)

        # Configurar colunas para expandirem
        for col in range(5):
            table.grid_columnconfigure(col, weight=1)

        # Cabeçalhos da tabela
        ttk.Label(table, text="Tipo de transação", style="TLabel").grid(
            row=0, column=0, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Data", style="TLabel").grid(
            row=0, column=1, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Categoria", style="TLabel").grid(
            row=0, column=2, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Conta", style="TLabel").grid(
            row=0, column=3, sticky="w", padx=5, pady=(0, 5)
        )
        ttk.Label(table, text="Valor", style="TLabel").grid(
            row=0, column=4, sticky="e", padx=5, pady=(0, 5)
        )

        # Lista de transações
        transactions = self.transaction_service.get_all_transactions()
        for i, transaction in enumerate(transactions, start=1):
            category = (
                transaction.category.name
                if isinstance(transaction, Expense) and transaction.category
                else ""
            )
            transaction_type = TransactionType.get_visual_label(
                transaction_type=transaction.transaction_type
            )

            ttk.Label(table, text=transaction_type, style="TLabel").grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )
            ttk.Label(
                table, text=transaction.date.strftime("%d/%m/%Y"), style="TLabel"
            ).grid(row=i, column=1, sticky="w", padx=5, pady=2)
            ttk.Label(table, text=category, style="TLabel").grid(
                row=i, column=2, sticky="w", padx=5, pady=2
            )
            ttk.Label(
                table,
                text=(
                    transaction.payment_method.name
                    if transaction.payment_method
                    else ""
                ),
                style="TLabel",
            ).grid(row=i, column=3, sticky="w", padx=5, pady=2)
            ttk.Label(table, text=f"R${transaction.amount}", style="TLabel").grid(
                row=i, column=4, sticky="e", padx=5, pady=2
            )

        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def refresh_transactions(self):
        """Atualiza a lista de transações"""
        # Encontra e destrói o frame da tabela (mantendo o cabeçalho)
        for widget in self.inner_frame.winfo_children():
            if widget != self.header_frame:
                widget.destroy()

        # Recria a lista de transações
        self.create_transaction_list()
