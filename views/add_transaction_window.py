import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from src.services.transaction_service import TransactionService
from src.models.transaction.income import Income
from src.models.transaction.expense import Expense
from views.add_category_window import AddCategoryWindow
from src.services.category_service import CategoryService
from src.services.payment_method_service import PaymentMethodService
from src.models.payment_method.payment_type import PaymentType


class AddTransactionWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Adicionar Transação")
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
        self.categories_data = {}

        self.transaction_service = TransactionService()
        self.category_service = CategoryService()
        self.payment_method_service = PaymentMethodService()
        self.payment_methods_data = {}

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
            text="Adicionar Transação",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors["light_gray"],
            fg=self.colors["dark_blue"],
        )
        title_label.pack(pady=(0, 20))

        # Canvas + Scrollbar
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(
            canvas_frame, bg=self.colors["light_gray"], highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame dentro do Canvas
        self.form_frame = tk.Frame(canvas, bg=self.colors["white"], padx=20, pady=20)
        self.form_frame_id = canvas.create_window(
            (0, 0), window=self.form_frame, anchor="nw"
        )

        # Atualiza o scrollregion quando o tamanho do frame mudar
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(self.form_frame_id, width=canvas.winfo_width())

        self.form_frame.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", on_configure)

        # Permite rolar com o mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Estilos e campos do formulário
        self.configure_styles()
        self.create_form_fields(self.form_frame)

        # Frame dos botões
        button_frame = tk.Frame(main_frame, bg=self.colors["light_gray"])
        button_frame.pack(fill="x", pady=(20, 0))

        save_button = ttk.Button(
            button_frame,
            text="Salvar",
            style="Blue.TButton",
            command=self.save_transaction,
        )
        save_button.pack(side="right", padx=5)

        cancel_button = ttk.Button(
            button_frame, text="Cancelar", style="Red.TButton", command=self.destroy
        )
        cancel_button.pack(side="right", padx=5)

        button_frame.pack_propagate(False)
        button_frame.configure(height=50)

    def configure_styles(self):
        """Configura os estilos dos widgets"""
        style = ttk.Style()
        style.configure(
            "TLabel",
            font=("Segoe UI", 10),
            background=self.colors["white"],
            foreground=self.colors["dark_blue"],
        )

        style.configure("TEntry", padding=5, relief="flat")
        style.configure("TCombobox", padding=5)

        style.configure(
            "Blue.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.colors["medium_blue"],
            foreground=self.colors["white"],
            padding=10,
            relief="flat",
        )

        style.map("Blue.TButton", background=[("active", self.colors["dark_blue"])])

        style.configure(
            "Red.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.colors["medium_red"],
            foreground=self.colors["white"],
            padding=10,
        )

        style.map("Red.TButton", background=[("active", self.colors["dark_red"])])

    def create_form_fields(self, parent):
        """Cria todos os campos do formulário"""
        # Armazena o frame principal para uso posterior
        self.main_form_frame = parent

        # Tipo de Transação
        ttk.Label(parent, text="Tipo de Transação *").pack(anchor="w", pady=(0, 5))
        self.transaction_types = ttk.Combobox(
            parent,
            values=["Receita", "Despesa"],
            font=("Segoe UI", 10),
            state="readonly",
        )
        self.transaction_types.pack(fill="x", pady=(0, 15))
        self.transaction_types.bind(
            "<<ComboboxSelected>>", self.on_transaction_type_change
        )

        # Data
        ttk.Label(parent, text="Data *").pack(anchor="w", pady=(0, 5))
        self.date_entry = DateEntry(
            parent,
            font=("Segoe UI", 10),
            background=self.colors["medium_blue"],
            foreground=self.colors["white"],
            borderwidth=2,
            date_pattern="dd/mm/yyyy",
        )
        self.date_entry.pack(fill="x", pady=(0, 15))

        # Valor
        ttk.Label(parent, text="Valor *").pack(anchor="w", pady=(0, 5))
        vcmd = (self.register(self.validate_numeric_input), "%P")
        self.entry_value = ttk.Entry(
            parent, font=("Segoe UI", 10), validate="key", validatecommand=vcmd
        )
        self.entry_value.pack(fill="x", pady=(0, 15))

        # Descrição
        ttk.Label(parent, text="Descrição").pack(anchor="w", pady=(0, 5))
        self.desc_entry = ttk.Entry(parent, font=("Segoe UI", 10))
        self.desc_entry.pack(fill="x", pady=(0, 15))

        # Frame para categorias (inicialmente oculto)
        self.categories_frame = tk.Frame(parent, bg=self.colors["white"])
        self.categories_frame.pack_forget()

        # Frame para campos de pagamento (inicialmente oculto)
        self.payment_frame = tk.Frame(parent, bg=self.colors["white"])
        self.payment_frame.pack_forget()

        # Frame para parcelas (inicialmente oculto)
        self.installments_frame = tk.Frame(parent, bg=self.colors["white"])
        self.installments_frame.pack_forget()

    def on_transaction_type_change(self, event=None):
        """Lida com a mudança no tipo de transação"""
        transaction_type = self.transaction_types.get()

        if transaction_type == "Despesa":
            self.show_payment_fields()
            self.show_categories()
        else:
            self.hide_payment_fields()
            self.hide_categories()

    def show_payment_fields(self):
        """Mostra os campos de pagamento"""
        # Remove os frames se já existirem
        self.payment_frame.pack_forget()
        self.installments_frame.pack_forget()

        # Recria o frame de pagamento
        self.payment_frame = tk.Frame(self.main_form_frame, bg=self.colors["white"])
        self.payment_frame.pack(fill="x", pady=(0, 15))

        payment_methods = self.payment_method_service.get_all_payment_methods()
        self.payment_methods_data = {pm.name: pm for pm in payment_methods}

        payment_names = list(self.payment_methods_data.keys())

        # Forma de Pagamento
        ttk.Label(self.payment_frame, text="Forma de Pagamento *").pack(
            anchor="w", pady=(0, 5)
        )
        self.payment_method = ttk.Combobox(
            self.payment_frame,
            values=payment_names,
            font=("Segoe UI", 10),
            state="readonly",
        )
        self.payment_method.pack(fill="x", pady=(0, 15))
        self.payment_method.bind("<<ComboboxSelected>>", self.on_payment_method_change)

    def hide_payment_fields(self):
        """Esconde os campos de pagamento"""
        self.payment_frame.pack_forget()
        self.installments_frame.pack_forget()

    def show_categories(self):
        """Mostra o campo de categorias com opção de exclusão"""
        # Remove os frames se já existirem
        if hasattr(self, "categories_frame"):
            self.categories_frame.pack_forget()

        # Recria o frame de categorias
        self.categories_frame = tk.Frame(self.main_form_frame, bg=self.colors["white"])
        self.categories_frame.pack(fill="x", pady=(0, 15))

        # Categoria
        ttk.Label(self.categories_frame, text="Categoria *").pack(
            anchor="w", pady=(0, 5)
        )

        # Obtém categorias existentes
        self.categories_data = {
            c.name: c for c in self.category_service.get_all_categories()
        }
        category_names = list(self.categories_data.keys())
        category_names.append("Adicionar nova categoria")

        # Cria o frame para o ícone e combobox
        self.combo_icon_frame = tk.Frame(self.categories_frame)
        self.combo_icon_frame.pack(fill="x", pady=(0, 15))

        # Cria o Combobox
        self.categories = ttk.Combobox(
            self.combo_icon_frame,
            values=category_names,
            font=("Segoe UI", 10),
            state="readonly",
        )

        self.categories.pack(side="left", fill="x", expand=True)

        # Ícone de lixeira (menu de contexto)
        self.trash_icon = tk.PhotoImage(file="views/icons/trash.png").subsample(40, 40)
        self.trash_button = tk.Button(
            self.combo_icon_frame,
            image=self.trash_icon,
            relief="flat",
            command=self.delete_category,
            cursor="hand2",
        )
        self.trash_button.pack(side="left", padx=(5, 0))
        self.trash_button.pack_forget()

        # Vincula os eventos
        self.categories.bind("<<ComboboxSelected>>", self.on_category_selected)
        self.categories_frame.pack(fill="x", pady=(0, 15))

    def on_category_selected(self, event=None):
        """Lida com a seleção de categoria"""
        selected = self.categories.get()

        if selected == "Adicionar nova categoria":
            self.show_add_category_window()
            self.categories.set("")
            self.trash_button.pack_forget()
        else:
            # Mostra o botão de lixeira para categorias normais
            self.trash_button.pack(side="right", padx=(5, 0))

    def show_category_context_menu(self):
        """Mostra menu de contexto com opção de excluir"""
        selected_category = self.categories.get()
        if not selected_category or selected_category == "Adicionar nova categoria":
            return

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(
            label=f"Excluir '{selected_category}'",
            command=lambda: self.delete_category(selected_category),
        )

        # Posiciona o menu próximo ao botão
        x = self.context_menu_btn.winfo_rootx()
        y = self.context_menu_btn.winfo_rooty() + self.context_menu_btn.winfo_height()
        menu.post(x, y)

    def delete_category(self):
        """Exclui a categoria selecionada"""
        selected_name = self.categories.get()
        if selected_name == "Adicionar nova categoria":
            return

        if tk.messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a categoria '{selected_name}'?\n"
            "Isso afetará todas as transações associadas.",
        ):
            try:
                selected_category = self.categories_data.get(selected_name)
                if selected_category:
                    self.category_service.delete_category(selected_category.id)

                    self.show_categories()
                tk.messagebox.showinfo("Sucesso", "Categoria excluída com sucesso!")
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Falha ao excluir categoria: {str(e)}")

    def show_add_category_window(self):
        """Abre a janela para adicionar nova categoria"""

        def update_categories(new_category):
            """Atualiza a lista de categorias"""
            if (
                new_category.name not in self.categories_data
                and new_category.name != "Adicionar nova categoria"
            ):
                self.categories_data[new_category.name] = new_category
                updated_names = list(self.categories_data.keys())
                updated_names.sort()
                updated_names.append("Adicionar nova categoria")
                self.categories["values"] = updated_names
                self.categories.set(new_category.name)

        AddCategoryWindow(self, callback=update_categories)

    def hide_categories(self):
        """Esconde o campo de categorias"""
        self.categories_frame.pack_forget()

    def show_installments_field(self):
        """Mostra o campo de parcelas"""
        # Remove o frame se já existir
        self.installments_frame.pack_forget()

        # Recria o frame de parcelas
        self.installments_frame = tk.Frame(
            self.main_form_frame, bg=self.colors["white"]
        )
        self.installments_frame.pack(fill="x", pady=(0, 15))

        # Parcelas
        ttk.Label(self.installments_frame, text="Número de Parcelas *").pack(
            anchor="w", pady=(0, 5)
        )
        vcmd_installments = (
            self.register(self.validate_numeric_input_installments),
            "%P",
        )
        self.installments = ttk.Entry(
            self.installments_frame,
            font=("Segoe UI", 10),
            validate="key",
            validatecommand=vcmd_installments,
        )
        self.installments.pack(fill="x", pady=(0, 15))

    def hide_installments_field(self):
        """Esconde o campo de parcelas"""
        self.installments_frame.pack_forget()
        if hasattr(self, "installments"):
            del self.installments
        self.installments = None

    def on_payment_method_change(self, event=None):
        """Lida com a mudança no método de pagamento"""
        selected_name = self.payment_method.get()
        if selected_name in self.payment_methods_data:
            selected_method = self.payment_methods_data[selected_name]
            if selected_method.payment_type == PaymentType.CREDIT:
                self.show_installments_field()
            else:
                self.hide_installments_field()

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

    def validate_numeric_input_installments(self, new_text):
        """Permite apenas números inteiros entre 1 e 360"""
        if not new_text:
            return True
        try:
            value = int(new_text)
            return 1 <= value <= 360
        except ValueError:
            return False

    def save_transaction(self):
        """Valida e salva a transação"""
        # Obter valores
        transaction_type = self.transaction_types.get()
        date = self.date_entry.get_date()
        value = self.entry_value.get()
        description = self.desc_entry.get()

        payment_method_name = (
            self.payment_method.get() if hasattr(self, "payment_method") else None
        )
        payment_method = (
            self.payment_methods_data.get(payment_method_name)
            if payment_method_name
            else None
        )

        category_name = self.categories.get() if hasattr(self, "categories") else None
        category = self.categories_data.get(category_name) if category_name else None

        installment = self.installments.get() if hasattr(self, "installment") else None

        # Validação
        errors = []
        value_str = self.entry_value.get()
        if not value_str:
            errors.append("Valor não pode estar vazio")
        else:
            try:
                value = float(value_str.replace(",", "."))
                if value <= 0:
                    errors.append("Valor deve ser positivo")
            except ValueError:
                errors.append("Valor inválido (use números com . ou , para decimais)")

        if not date:
            errors.append("Selecione uma data")
        if not transaction_type:
            errors.append("Selecione um tipo de transação")

        if transaction_type == "Despesa":
            if not category:
                errors.append("Selecione uma categoria")
            if not payment_method:
                errors.append("Selecione uma forma de pagamento")
            if payment_method == "Crédito":
                try:
                    installment = int(installment) if installment else 0
                    if installment <= 0 or installment > 360:
                        errors.append("Número de parcelas deve ser entre 1 e 360")
                except (ValueError, TypeError):
                    errors.append("Número de parcelas inválido")

        if errors:
            tk.messagebox.showerror(
                "Erro de Validação",
                "Corrija os seguintes erros:\n- " + "\n- ".join(errors),
            )
            return

        # Formatar dados
        transaction_data = {
            "date": date.strftime("%Y-%m-%d"),
            "amount": value,
            "description": description,
        }

        try:
            if transaction_type == "Receita":
                transaction = Income.from_dict(transaction_data)
            elif transaction_type == "Despesa":
                transaction_data.update(
                    {
                        "category": category,
                        "total_installments": int(installment) if installment else 1,
                        "current_installment": 1,
                        "payment_method": payment_method,
                    }
                )
                transaction = Expense.from_dict(transaction_data)
            else:
                raise ValueError("Tipo de transação inválido")

            result = self.transaction_service.add_transaction(transaction)
            if not result:
                raise Exception("Falha ao salvar transação")

            tk.messagebox.showinfo("Sucesso", f"Transação adicionada com sucesso!")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Falha ao salvar transação: {str(e)}")
