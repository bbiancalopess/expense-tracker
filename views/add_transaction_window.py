import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

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
        
        self.configure(bg=self.colors["light_gray"])
        self.create_widgets()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 3) - (height // 3)
        self.geometry(f'+{x}+{y}')
    
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
            fg=self.colors["dark_blue"]
        )
        title_label.pack(pady=(0, 20))

        # Canvas + Scrollbar
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(expand=True, fill="both")

        canvas = tk.Canvas(canvas_frame, bg=self.colors["light_gray"], highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame dentro do Canvas
        self.form_frame = tk.Frame(canvas, bg=self.colors["white"], padx=20, pady=20)
        self.form_frame_id = canvas.create_window((0, 0), window=self.form_frame, anchor="nw")

        # Atualiza o scrollregion quando o tamanho do frame mudar
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(self.form_frame_id, width=canvas.winfo_width())

        self.form_frame.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", on_configure)

        # Permite rolar com o mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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
            command=self.save_transaction
        )
        save_button.pack(side="right", padx=5)

        cancel_button = ttk.Button(
            button_frame,
            text="Cancelar",
            style="Red.TButton",
            command=self.destroy
        )
        cancel_button.pack(side="right", padx=5)

        button_frame.pack_propagate(False)
        button_frame.configure(height=50)

    def configure_styles(self):
        """Configura os estilos dos widgets"""
        style = ttk.Style()
        style.configure("TLabel", 
                      font=("Segoe UI", 10),
                      background=self.colors["white"],
                      foreground=self.colors["dark_blue"])
        
        style.configure("TEntry", padding=5, relief="flat")
        style.configure("TCombobox", padding=5)
        
        style.configure("Blue.TButton",
                      font=("Segoe UI", 10, "bold"),
                      background=self.colors["medium_blue"],
                      foreground=self.colors["white"],
                      padding=10,
                      relief="flat")
        
        style.map("Blue.TButton",
                background=[("active", self.colors["dark_blue"])])

        style.configure("Red.TButton",
              font=("Segoe UI", 10, "bold"),
              background=self.colors["medium_red"],
              foreground=self.colors["white"],
              padding=10)

        style.map("Red.TButton",
                background=[("active", self.colors["dark_red"])])
    
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
            state="readonly"
        )
        self.transaction_types.pack(fill="x", pady=(0, 15))
        self.transaction_types.bind("<<ComboboxSelected>>", self.on_transaction_type_change)

        # Data
        ttk.Label(parent, text="Data *").pack(anchor="w", pady=(0, 5))
        self.date_entry = DateEntry(
            parent,
            font=("Segoe UI", 10),
            background=self.colors["medium_blue"],
            foreground=self.colors["white"],
            borderwidth=2,
            date_pattern='dd/mm/yyyy'
        )
        self.date_entry.pack(fill="x", pady=(0, 15))
        
        # Valor
        ttk.Label(parent, text="Valor *").pack(anchor="w", pady=(0, 5))
        vcmd = (self.register(self.validate_numeric_input), '%P')
        self.entry_value = ttk.Entry(
            parent, 
            font=("Segoe UI", 10),
            validate="key",
            validatecommand=vcmd
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
        
        # Forma de Pagamento
        ttk.Label(self.payment_frame, text="Forma de Pagamento *").pack(anchor="w", pady=(0, 5))
        self.payment_method = ttk.Combobox(
            self.payment_frame,
            values=["Débito", "Crédito"],
            font=("Segoe UI", 10),
            state="readonly"
        )
        self.payment_method.pack(fill="x", pady=(0, 15))
        self.payment_method.bind("<<ComboboxSelected>>", self.on_payment_method_change)

    def hide_payment_fields(self):
        """Esconde os campos de pagamento"""
        self.payment_frame.pack_forget()
        self.installments_frame.pack_forget()

    def show_categories(self):
        """Mostra o campo de categorias"""
        # Remove os frames se já existirem
        self.categories_frame.pack_forget()
        
        # Recria o frame de categorias
        self.categories_frame = tk.Frame(self.main_form_frame, bg=self.colors["white"])
        self.categories_frame.pack(fill="x", pady=(0, 15))
        
        # Categoria
        ttk.Label(self.categories_frame, text="Categoria *").pack(anchor="w", pady=(0, 5))
        self.categories = ttk.Combobox(
            self.categories_frame,
            values=["Alimentação", "Transporte", "Saúde", "Lazer", "Outros"],
            font=("Segoe UI", 10),
            state="readonly"
        )
        self.categories.pack(fill="x", pady=(0, 15))
        self.categories_frame.pack(fill="x", pady=(0, 15))

    def hide_categories(self):
        """Esconde o campo de categorias"""
        self.categories_frame.pack_forget()
    
    def show_installments_field(self):
        """Mostra o campo de parcelas"""
        # Remove o frame se já existir
        self.installments_frame.pack_forget()
        
        # Recria o frame de parcelas
        self.installments_frame = tk.Frame(self.main_form_frame, bg=self.colors["white"])
        self.installments_frame.pack(fill="x", pady=(0, 15))
        
        # Parcelas
        ttk.Label(self.installments_frame, text="Número de Parcelas *").pack(anchor="w", pady=(0, 5))
        vcmd_installments = (self.register(self.validate_numeric_input_installments), '%P')
        self.installments = ttk.Entry(
            self.installments_frame,
            font=("Segoe UI", 10),
            validate="key",
            validatecommand=vcmd_installments
        )
        self.installments.pack(fill="x", pady=(0, 15))

    def hide_installments_field(self):
        """Esconde o campo de parcelas"""
        self.installments_frame.pack_forget()
        if hasattr(self, 'installments'):
            del self.installments
        self.installments = None


    def on_payment_method_change(self, event=None):
        """Lida com a mudança no método de pagamento"""
        if self.payment_method.get() == "Crédito":
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
            value_str = new_text.replace(',', '.')
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
        payment_method = self.payment_method.get()
        category = self.categories.get()
        installment = self.installments.get()
        
        # Validação
        errors = []
        value_str = self.entry_value.get()
        if not value_str:
            errors.append("Valor não pode estar vazio")
        else:
            try:
                value = float(value_str.replace(',', '.'))
                if value <= 0:
                    errors.append("Valor deve ser positivo")
            except ValueError:
                errors.append("Valor inválido (use números com . ou , para decimais)")
        if not category:
            errors.append("Selecione uma categoria")
        if not payment_method:
            errors.append("Selecione uma forma de pagamento")
        if not transaction_type:
            errors.append("Selecione um tipo de transação")
        if not date:
            errors.append("Selecione uma data")
        
        if payment_method == "Crédito" and not hasattr(self, 'installments'):
            errors.append("Selecione o número de parcelas")
        
        if int(installment) > 360 or int(installment) <= 0 :
            errors.append("Valor inválido, o número de parcelas tem que estar entre 0 e 360")
        
        if errors:
            tk.messagebox.showerror(
                "Erro de Validação",
                "Corrija os seguintes erros:\n- " + "\n- ".join(errors)
            )
            return
        
        # Formatar dados
        transaction_data = {
            "type": transaction_type,
            "date": date.strftime("%d/%m/%Y"),
            "value": value,
            "description": description,
            "payment_method": payment_method,
            "category": category,
            "installments": getattr(self, 'installments', None) and self.installments.get()
        }
        
        # Aqui você conectaria com o backend para salvar
        print("Transação salva:", transaction_data)

        # Fechar a janela após salvar
        self.destroy()