import tkinter as tk
from tkinter import ttk, messagebox
from src.services.payment_method_service import PaymentMethodService
from src.models.payment_method.debit import Debit
from src.models.payment_method.credit import Credit
from src.models.payment_method.payment_type import PaymentType


class AddAccountWindow(tk.Toplevel):
    def __init__(self, master=None, wallet_window=None):
        super().__init__(master)
        self.wallet_window = wallet_window
        self.title("Adicionar Nova Conta")
        self.geometry("650x700")
        self.minsize(500, 600)

        # Centraliza a janela
        self.center_window()

        # Paleta de cores
        self.colors = {
            "dark_blue": "#022b3a",
            "medium_blue": "#1f7a8c",
            "light_blue": "#bfdbf7",
            "light_gray": "#e1e5f2",
            "white": "#ffffff",
            "dark_red": "#9b2226",
            "medium_red": "#ae2012",
        }

        self.payment_method_service = PaymentMethodService()

        self.configure(bg=self.colors["light_gray"])
        self.create_widgets()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 3) - (height // 3)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.colors["light_gray"])
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Título
        title_label = tk.Label(
            main_frame,
            text="Adicionar Nova Conta",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["light_gray"],
            fg=self.colors["dark_blue"],
        )
        title_label.pack(pady=(0, 20))

        # Frame do formulário
        self.form_frame = tk.Frame(
            main_frame, bg=self.colors["white"], padx=20, pady=20
        )
        self.form_frame.pack(fill="both", expand=True)

        self.configure_styles()
        self.create_form_fields()

        # Frame dos botões
        button_frame = tk.Frame(main_frame, bg=self.colors["light_gray"])
        button_frame.pack(fill="x", pady=(20, 0))

        save_button = ttk.Button(
            button_frame, text="Salvar", style="Blue.TButton", command=self.save_account
        )
        save_button.pack(side="right", padx=5)

        cancel_button = ttk.Button(
            button_frame, text="Cancelar", style="Red.TButton", command=self.destroy
        )
        cancel_button.pack(side="right", padx=5)

        button_frame.pack_propagate(False)
        button_frame.configure(height=50)

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo dos botões
        style.configure(
            "Blue.TButton",
            font=("Segoe UI", 10),
            padding=8,
            background=self.colors["medium_blue"],
            foreground=self.colors["white"],
            width=15,
            anchor="w",
        )

        style.map("Blue.TButton", background=[("active", self.colors["dark_blue"])])

        style.configure(
            "Red.TButton",
            font=("Segoe UI", 10),
            padding=8,
            background=self.colors["medium_red"],
            foreground=self.colors["white"],
            width=15,
            anchor="w",
        )

        style.map("Red.TButton", background=[("active", self.colors["dark_red"])])

    def create_form_fields(self):
        """Cria os campos do formulário"""
        # Campo para o nome do banco
        bank_label = tk.Label(
            self.form_frame,
            text="Nome *",
            bg=self.colors["white"],
            fg=self.colors["dark_blue"],
        )
        bank_label.pack(anchor="w", pady=(10, 0))
        self.bank_entry = ttk.Entry(self.form_frame)
        self.bank_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Campo para o saldo
        balance_label = tk.Label(
            self.form_frame,
            text="Saldo Inicial *",
            bg=self.colors["white"],
            fg=self.colors["dark_blue"],
        )
        balance_label.pack(anchor="w", pady=(10, 0))
        vcmd_balance = (self.register(self.validate_numeric_input), "%P")
        self.balance_entry = ttk.Entry(
            self.form_frame, validate="key", validatecommand=vcmd_balance
        )
        self.balance_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Campo para o tipo de conta
        account_type_label = tk.Label(
            self.form_frame,
            text="Tipo de Conta *",
            bg=self.colors["white"],
            fg=self.colors["dark_blue"],
        )
        account_type_label.pack(anchor="w", pady=(10, 0))
        self.account_type_var = tk.StringVar()
        self.account_type_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.account_type_var,
            values=["Débito", "Crédito"],
            state="readonly",
        )
        self.account_type_combobox.pack(fill="x", padx=5, pady=(0, 10))
        self.account_type_combobox.bind(
            "<<ComboboxSelected>>", self.on_account_type_change
        )

        # Frame para campos de cartão de crédito (inicialmente oculto)
        self.credit_card_frame = tk.Frame(self.form_frame, bg=self.colors["white"])
        self.credit_card_frame.pack_forget()

    def on_account_type_change(self, event=None):
        """Lida com a mudança no tipo de conta"""
        account_type = self.account_type_var.get()

        if account_type == "Crédito":
            self.show_credit_card_fields()
        else:
            self.hide_credit_card_fields()

    def show_credit_card_fields(self):
        """Mostra os campos específicos para cartão de crédito"""
        self.hide_credit_card_fields()

        self.credit_card_frame = tk.Frame(self.form_frame, bg=self.colors["white"])
        self.credit_card_frame.pack(fill="x", pady=(10, 0))

        self.limit_label = tk.Label(
            self.credit_card_frame,
            text="Limite *",
            bg=self.colors["white"],
            fg=self.colors["dark_blue"],
        )
        self.limit_label.pack(anchor="w", pady=(5, 0))

        self.limit_var = tk.StringVar()
        vcmd_limit = (self.register(self.validate_numeric_input), "%P")
        self.limit_entry = ttk.Entry(
            self.credit_card_frame,
            textvariable=self.limit_var,
            validate="key",
            validatecommand=vcmd_limit,
        )
        self.limit_entry.pack(fill="x", padx=5, pady=(0, 10))

        # Dia de vencimento
        due_day_label = tk.Label(
            self.credit_card_frame,
            text="Dia de Vencimento *",
            bg=self.colors["white"],
            fg=self.colors["dark_blue"],
        )
        due_day_label.pack(anchor="w", pady=(5, 0))

        self.due_day_var = tk.StringVar()
        vcmd_due = (self.register(self.validate_day_input), "%P")
        self.due_day_entry = ttk.Entry(
            self.credit_card_frame,
            textvariable=self.due_day_var,
            validate="key",
            validatecommand=vcmd_due,
            width=15,
        )
        self.due_day_entry.pack(anchor="w", pady=(0, 10))

        # Dia de fechamento
        closing_day_label = tk.Label(
            self.credit_card_frame,
            text="Dia de Fechamento *",
            bg=self.colors["white"],
            fg=self.colors["dark_blue"],
        )
        closing_day_label.pack(anchor="w", pady=(5, 0))

        self.closing_day_var = tk.StringVar()
        vcmd_close = (self.register(self.validate_day_input), "%P")
        self.closing_day_entry = ttk.Entry(
            self.credit_card_frame,
            textvariable=self.closing_day_var,
            validate="key",
            validatecommand=vcmd_close,
            width=15,
        )
        self.closing_day_entry.pack(anchor="w", pady=(0, 10))

    def hide_credit_card_fields(self):
        """Esconde os campos de cartão de crédito"""
        self.credit_card_frame.pack_forget()

    def validate_numeric_input(self, new_text):
        """Permite apenas números, ponto ou vírgula decimal"""
        if not new_text:  # Permite campo vazio
            return True
        # Verifica se o texto é um número válido
        try:
            # Substitui vírgula por ponto para validação
            value_str = new_text.replace(",", ".")
            float(value_str)
            return True
        except ValueError:
            return False

    def validate_day_input(self, new_text):
        """Valida se o input é um dia válido (1-31)"""
        if not new_text:  # Permite campo vazio temporariamente
            return True

        # Verifica se contém apenas dígitos
        if not new_text.isdigit():
            return False

        # Converte para inteiro e verifica o intervalo
        try:
            day = int(new_text)
            return 1 <= day <= 31
        except ValueError:
            return False

    def save_account(self):
        """Valida e salva os dados da nova conta"""
        # Obter valores
        bank = self.bank_entry.get()
        balance = self.balance_entry.get()
        account_type = self.account_type_var.get()

        # Validação básica
        errors = []
        if not bank:
            errors.append("Nome da conta é obrigatório")
        if not account_type:
            errors.append("Tipo de conta é obrigatório")
        if not balance:
            errors.append("Saldo inicial é obrigatório")
        elif not self.validate_numeric_input(balance):
            errors.append("Saldo deve ser um valor numérico")
        if float(balance) < 0:
            errors.append("Saldo deve ser maior que 0")

        # Validação específica para cartão de crédito
        due_day = None
        closing_day = None
        if account_type == "Crédito":
            due_day = self.due_day_var.get()
            closing_day = self.closing_day_var.get()
            credit_limit = self.limit_var.get()

            if credit_limit < balance:
                errors.append(
                    "Limite de crédito não pode ser maior que o saldo inicial"
                )

            if not credit_limit:
                errors.append("Limite é obrigatório para cartões de crédito")
            if not due_day:
                errors.append("Dia de vencimento é obrigatório para cartões de crédito")
            elif not self.validate_day_input(due_day):
                errors.append("Dia de vencimento deve ser entre 1 e 31")

            if not closing_day:
                errors.append("Dia de fechamento é obrigatório para cartões de crédito")
            elif not self.validate_day_input(closing_day):
                errors.append("Dia de fechamento deve ser entre 1 e 31")

        if errors:
            messagebox.showerror(
                "Erro de Validação",
                "Corrija os seguintes erros:\n- " + "\n- ".join(errors),
            )
            return

        # Formatar dados
        try:
            balance_value = float(balance)
        except ValueError:
            balance_value = 0.0

        account_data = {
            "name": bank,
            "balance": balance_value,
            "type": PaymentType.DEBIT,
        }

        # Adiciona dados específicos de cartão de crédito
        if account_type == "Crédito":
            account_data.update(
                {
                    "due_day": int(due_day),
                    "closing_day": int(closing_day),
                    "type": PaymentType.CREDIT,
                    "credit_limit": float(credit_limit),
                }
            )

        if account_data["type"] == PaymentType.DEBIT:
            self.payment_method_service.add_payment_method(
                payment=Debit().from_dict(account_data)
            )
        elif account_data["type"] == PaymentType.CREDIT:
            self.payment_method_service.add_payment_method(
                payment=Credit().from_dict(account_data)
            )
        else:
            messagebox.showerror("Falha ao salvar. Tipo de conta inválido.")

        self.wallet_window.refresh()
        # Fecha a janela
        self.destroy()
