import tkinter as tk
from tkinter import ttk, messagebox
from views.add_account_window import AddAccountWindow
from src.services.payment_method_service import PaymentMethodService
from src.services.transaction_service import TransactionService
from src.models.payment_method.payment_type import PaymentType


class WalletWindow(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.parent = parent

        self.payment_method_service = PaymentMethodService()
        self.transactions_service = TransactionService()
        self.create_widgets()

    def open_add_account_window(self):
        if hasattr(self, "_add_window") and self._add_window.winfo_exists():
            self._add_window.lift()
            return

        self._add_window = AddAccountWindow(master=self.parent, wallet_window=self)
        self._add_window.grab_set()

    def create_widgets(self):
        contas = self.payment_method_service.get_all_payment_methods()
        incomes_and_expenses = (
            self.transactions_service.find_current_month_totals_by_payment_method()
        )
        total_balance = 0.0
        for c in contas:
            total_balance += c.balance

        total_incomes = 0.0
        total_expenses = 0.0
        for ie in incomes_and_expenses:
            total_incomes += ie["income"]
            total_expenses += ie["expense"]

        # Frame principal que ocupa todo o espaço
        main_frame = tk.Frame(self, bg=self.color_palette["light_gray"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header com saldo e valores
        header_frame = tk.Frame(
            main_frame, bg=self.color_palette["white"], padx=20, pady=15
        )
        header_frame.pack(fill="x", pady=(0, 20))

        # Saldo total
        saldo_frame = tk.Frame(header_frame, bg=self.color_palette["white"])
        saldo_frame.pack(side="left", fill="y")

        ttk.Label(
            saldo_frame,
            text="Saldo em conta",
            style="Title.TLabel",
            background=self.color_palette["white"],
        ).pack(anchor="w")
        ttk.Label(saldo_frame, text=f"R$ {total_balance:,.2f}", style="TLabel").pack(
            anchor="w", pady=(5, 0)
        )

        # Receitas e Despesas
        values_frame = tk.Frame(header_frame, bg=self.color_palette["white"])
        values_frame.pack(side="right", fill="y")

        # Receitas
        receitas_frame = tk.Frame(values_frame, bg=self.color_palette["white"])
        receitas_frame.pack(side="left", padx=20)
        ttk.Label(receitas_frame, text="Receitas", style="TLabel").pack(anchor="e")
        ttk.Label(receitas_frame, text=f"R$ {total_incomes:,.2f}", style="TLabel").pack(
            anchor="e"
        )

        # Despesas
        despesas_frame = tk.Frame(values_frame, bg=self.color_palette["white"])
        despesas_frame.pack(side="left", padx=20)
        ttk.Label(despesas_frame, text="Despesas", style="TLabel").pack(anchor="e")
        ttk.Label(
            despesas_frame, text=f"R$ {total_expenses:,.2f}", style="TLabel"
        ).pack(anchor="e")

        # Frame para conteúdo rolável
        canvas = tk.Canvas(
            main_frame, bg=self.color_palette["light_gray"], highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.color_palette["light_gray"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )

        def resize_scrollable_frame(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botão Adicionar Conta
        add_btn = ttk.Button(
            scrollable_frame,
            text="Adicionar conta",
            style="TButton",
            command=self.open_add_account_window,
        )
        add_btn.pack(padx=15, pady=(0, 20), anchor="e")

        # Contas
        contas_frame = tk.Frame(
            scrollable_frame, bg=self.color_palette["white"], padx=20, pady=15
        )
        contas_frame.pack(fill="both", pady=(0, 10), expand=True)

        ttk.Label(
            contas_frame,
            text="Contas",
            style="Title.TLabel",
            background=self.color_palette["white"],
        ).pack(anchor="w")

        total_amount_debit = 0.0
        for conta in contas:
            if conta.payment_type == PaymentType.DEBIT:
                conta_item = tk.Frame(
                    contas_frame, bg=self.color_palette["light_gray"], padx=10, pady=8
                )
                conta_item.pack(fill="x", pady=5, expand=True)

                name_frame = tk.Frame(conta_item, bg=self.color_palette["light_gray"])
                name_frame.pack(side="left", fill="x", expand=True)
                ttk.Label(
                    name_frame,
                    text=conta.name,
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(side="left")

                ttk.Label(
                    conta_item,
                    text=f"R$ {conta.balance:,.2f}",
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(side="left")
                # Botão de ícone de lixeira
                trash_icon = tk.PhotoImage(file="views/icons/trash.png").subsample(
                    35, 35
                )
                trash_button = tk.Button(
                    conta_item,
                    image=trash_icon,
                    relief="flat",
                    borderwidth=0,
                    cursor="hand2",
                    command=lambda c_id=conta.id: self.remove_account(c_id),
                )
                trash_button.image = trash_icon
                trash_button.pack(side="right", padx=10)
                total_amount_debit += conta.balance

        ttk.Label(
            contas_frame, text=f"Total R$ {total_amount_debit:,.2f}", style="TLabel"
        ).pack(anchor="e", pady=5)

        # Cartões
        cartoes_frame = tk.Frame(
            scrollable_frame, bg=self.color_palette["white"], padx=20, pady=15
        )
        cartoes_frame.pack(fill="both", expand=True)

        ttk.Label(
            cartoes_frame,
            text="Cartões de crédito",
            style="Title.TLabel",
            background=self.color_palette["white"],
        ).pack(anchor="w")

        total_amount_credit = 0.0
        for conta in contas:
            if conta.payment_type == PaymentType.CREDIT:
                cartao_item = tk.Frame(
                    cartoes_frame, bg=self.color_palette["light_gray"], padx=10, pady=8
                )
                cartao_item.pack(fill="x", pady=5, expand=True)

                info_frame = tk.Frame(cartao_item, bg=self.color_palette["light_gray"])
                info_frame.pack(side="left", fill="x", expand=True)
                ttk.Label(
                    info_frame,
                    text=conta.name,
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(anchor="w")
                ttk.Label(
                    info_frame,
                    text=f"Limite R$ {conta.credit_limit:,.2f}",
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(anchor="w")
                ttk.Label(
                    info_frame,
                    text=f"Vencimento dia {conta.due_day}",
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(anchor="w")
                ttk.Label(
                    info_frame,
                    text=f"Fechamento dia {conta.closing_day}",
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(anchor="w")
                ttk.Label(
                    cartao_item,
                    text=f"R$ {conta.balance:,.2f}",
                    style="TLabel",
                    background=self.color_palette["light_gray"],
                ).pack(side="left")
                # Botão de ícone de lixeira
                trash_icon = tk.PhotoImage(file="views/icons/trash.png").subsample(
                    35, 35
                )
                trash_button = tk.Button(
                    cartao_item,
                    image=trash_icon,
                    relief="flat",
                    borderwidth=0,
                    cursor="hand2",
                    command=lambda c_id=conta.id: self.remove_account(c_id),
                )
                trash_button.image = trash_icon
                trash_button.pack(side="right", padx=10)
                total_amount_credit += conta.balance

        ttk.Label(
            cartoes_frame, text=f"Total R$ {total_amount_credit:,.2f}", style="TLabel"
        ).pack(anchor="e", pady=5)

        # Configurar scroll com mouse
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def remove_account(self, account_id):
        confirm = tk.messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja remover esta conta?"
        )
        if confirm:
            self.payment_method_service.delete_payment_method(account_id)
            self.refresh()
