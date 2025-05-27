import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from src.services.transaction_service import TransactionService
from src.models.transaction.transaction_type import TransactionType
from src.models.transaction.expense import Expense


class TransactionsPanel(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.transaction_service = TransactionService()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.color_palette["light_gray"])
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            main_frame, bg=self.color_palette["white"], highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas, bg=self.color_palette["white"])

        canvas.create_window(
            (0, 0), window=inner_frame, anchor="nw", tags="inner_frame"
        )

        canvas.bind(
            "<Configure>", lambda e: canvas.itemconfig("inner_frame", width=e.width)
        )

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig("inner_frame", width=event.width)

        inner_frame.bind("<Configure>", on_frame_configure)

        def on_canvas_configure(event):
            canvas.itemconfig("inner_frame", width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)

        header_frame = tk.Frame(
            inner_frame, bg=self.color_palette["white"], padx=20, pady=20
        )
        header_frame.pack(fill="x", pady=(0, 20))

        # Título
        title = ttk.Label(
            header_frame,
            text="Transações",
            style="Title.TLabel",
            background=self.color_palette["white"],
        )
        title.pack(side="left", anchor="w")

        dates_frame = tk.Frame(header_frame, bg=self.color_palette["white"])
        dates_frame.pack(side="right", anchor="e")

        # Campo "De"
        ttk.Label(dates_frame, text="De:", style="TLabel").pack(
            side="left", padx=(0, 5)
        )
        self.date_entry = DateEntry(
            dates_frame,
            font=("Segoe UI", 10),
            background=self.color_palette["medium_blue"],
            foreground=self.color_palette["white"],
            borderwidth=2,
            date_pattern="dd/mm/yyyy",
        )
        self.date_entry.pack(side="left", padx=(0, 15))

        # Campo "Até"
        ttk.Label(dates_frame, text="Até:", style="TLabel").pack(
            side="left", padx=(0, 5)
        )
        self.date_entry_until = DateEntry(
            dates_frame,
            font=("Segoe UI", 10),
            background=self.color_palette["medium_blue"],
            foreground=self.color_palette["white"],
            borderwidth=2,
            date_pattern="dd/mm/yyyy",
        )
        self.date_entry_until.pack(side="left")

        # Tabela com headers e valores
        table = tk.Frame(inner_frame, bg=self.color_palette["white"])
        table.pack(fill="both", expand=True)

        # Configurar colunas para expandirem
        for col in range(5):
            table.grid_columnconfigure(col, weight=1)

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
                transaction.category.name if isinstance(transaction, Expense) else ""
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

        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
