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
            "white": "#ffffff"
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
        # Frame principal com scrollbar
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
        
        # Frame do formulário com scrollbar
        form_frame = tk.Frame(main_frame, bg=self.colors["white"], padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)
        
        # Configurar estilo
        self.configure_styles()
        
        # Campos do formulário
        self.create_form_fields(form_frame)
        
        # Frame dos botões
        button_frame = tk.Frame(form_frame, bg=self.colors["white"])
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Botões
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
            style="Blue.TButton",
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
        self.transaction_types.current(0)  # Seleciona o primeiro item por padrão
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
        self.entry_value = ttk.Entry(parent, font=("Segoe UI", 10))
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
        self.categories.bind("<<ComboboxSelected>>", self.on_category_change)
        self.categories_frame.pack(fill="x", pady=(0, 15))

    def hide_categories(self):
        """Esconde o campo de categorias"""
        self.categories_frame.pack_forget()
    
    def show_installments_field(self):
        """Mostra o campo de parcelas"""
        self.installments_frame.pack_forget()
        
        self.installments_frame

    def on_payment_method_change(self, event=None):
        """Lida com a mudança no método de pagamento"""
        if self.payment_method.get() == "Crédito":
            self.show_installments_field()
        else:
            self.hide_installments_field()
    
    def save_transaction(self):
        """Valida e salva a transação"""
        # Obter valores
        transaction_type = self.transaction_types.get()
        date = self.date_entry.get_date()
        value = self.entry_value.get()
        description = self.desc_entry.get()
        payment_method = self.payment_method.get()
        category = self.categories.get()
        
        # Validação
        errors = []
        if not value or not value.replace(',', '').replace('.', '').isdigit():
            errors.append("Valor inválido")
        if not category:
            errors.append("Selecione uma categoria")
        if not payment_method:
            errors.append("Selecione uma forma de pagamento")
        if not transaction_type:
            errors.append("Selecione um tipo de transação")
        if not date:
            errors.append("Selecione uma data")
        
        # Validação específica para crédito
        if payment_method == "Crédito" and not hasattr(self, 'installments'):
            errors.append("Selecione o número de parcelas")
        
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
            "value": float(value.replace(',', '.')),
            "description": description,
            "payment_method": payment_method,
            "category": category,
            "installments": getattr(self, 'installments', None) and self.installments.get()
        }
        
        # Aqui você conectaria com o backend para salvar
        print("Transação salva:", transaction_data)
        self.destroy()