import tkinter as tk
from tkinter import ttk
from views.components.transactions_panel import TransactionsPanel
from views.add_transaction_window import AddTransactionWindow
from views.wallet_window import WalletWindow
from views.metrics_window import MetricsWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1000x650")
        self.resizable(True, True)
        self.minsize(800, 600)
        self.center_window()

        # Configuração da paleta de cores
        self.color_palette = {
            "dark_blue": "#022b3a",
            "medium_blue": "#1f7a8c",
            "light_blue": "#bfdbf7",
            "light_gray": "#e1e5f2",
            "white": "#ffffff",
            "sidebar": "#1f7a8c",
            "dark_red": "#9b2226",
            "medium_red": "#ae2012"
        }
        
        self.configure_style()
        self.configure(bg=self.color_palette["light_gray"])
        self.create_widgets()

    def center_window(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = (width - 1000) // 2 
        y = (height - 650) // 3  
        self.geometry(f"+{x}+{y}")

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo dos botões do sidebar
        style.configure("Sidebar.TButton",
            font=("Segoe UI", 12),
            padding=10,
            background=self.color_palette["sidebar"],
            foreground=self.color_palette["white"],
            width=15,
            anchor="w")
        
        style.map("Sidebar.TButton",
            background=[("active", self.color_palette["dark_blue"])])
        
        # Estilo dos botões normais
        style.configure("TButton",
            font=("Segoe UI", 10),
            padding=8,
            background=self.color_palette["medium_blue"],
            foreground=self.color_palette["white"]),

        
        style.map("TButton",
            background=[("active", self.color_palette["dark_blue"])])

        # Estilo do botão "Sair"
        style.configure("Exit.TButton",
            font=("Segoe UI", 12),
            padding=10,
            background=self.color_palette["medium_red"],
            foreground=self.color_palette["white"],
            width=15,
            anchor="w")

        style.map("Exit.TButton",
            background=[("active", self.color_palette["dark_red"])])
        
        style.configure("TLabel",
            font=("Segoe UI", 12),
            background=self.color_palette["white"],
            foreground=self.color_palette["dark_blue"])
        
        style.configure("Title.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground=self.color_palette["dark_blue"])
            

    def create_widgets(self):
        # Frame principal que contém sidebar e content
        main_container = tk.Frame(self, bg=self.color_palette["light_gray"])
        main_container.pack(expand=True, fill="both")

        # Sidebar
        sidebar = tk.Frame(main_container, bg=self.color_palette["sidebar"], width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_label = tk.Label(sidebar, 
            text="Expense Tracker",
            bg=self.color_palette["sidebar"],
            fg=self.color_palette["white"],
            font=("Segoe UI", 14, "bold"),
            pady=20)
        logo_label.pack(fill="x")

        buttons = [
            ("Home", self.show_home),

            ("Carteira", self.open_wallet),
            ("Métricas", self.open_metrics),
        ]

        for text, command in buttons:
            btn = ttk.Button(sidebar, text=text, command=command, style="Sidebar.TButton")
            btn.pack(pady=5, padx=10, fill="x")

        exit_btn = ttk.Button(sidebar, text="Sair", command=self.quit, style="Exit.TButton")
        exit_btn.pack(side="bottom", pady=10, padx=10, fill="x")

        # Frame de conteúdo principal que será trocado
        self.content_frame = tk.Frame(main_container, bg=self.color_palette["light_gray"])
        self.content_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Carregar conteúdo inicial
        self.show_home()

    def switch_content(self, new_frame_class):
        # Remove o conteúdo atual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Insere novo conteúdo
        frame = new_frame_class(self.content_frame, self.color_palette)
        frame.pack(expand=True, fill="both")

    def show_home(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title = ttk.Label(self.content_frame, text="Tela inicial", style="Title.TLabel")
        title.pack(pady=(0, 20), anchor="w")

        self.transactions_panel = TransactionsPanel(self.content_frame, self.color_palette)
        self.transactions_panel.pack(expand=True, fill="both")

        add_btn = ttk.Button(self.content_frame,
                            text="Adicionar Transação",
                            command=self.open_add_transaction,
                            style="TButton")
        add_btn.pack(pady=20, ipadx=20, ipady=5)


    def open_add_transaction(self):
        AddTransactionWindow(self)
    
    def open_wallet(self):
        self.switch_content(WalletWindow)


    def open_metrics(self):
        self.switch_content(MetricsWindow)

    def quit(self):
        self.destroy()