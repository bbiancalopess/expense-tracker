import tkinter as tk
from tkinter import ttk

class WalletFrame(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"], padx=10, pady=10)
        self.color_palette = color_palette
        self.create_widgets()

    def create_widgets(self):
        # Frame interno
        inner_frame = tk.Frame(self, bg=self.color_palette["white"], padx=20, pady=20)
        inner_frame.pack(expand=True, fill="both")

        # Título
        title = ttk.Label(inner_frame, 
                        text="Carteira",
                        style="TLabel")
        title.pack(pady=(0, 10))

        # Botões
        btn_frame = tk.Frame(inner_frame, bg=self.color_palette["white"])
        btn_frame.pack(fill="x", pady=10)

        add_btn = ttk.Button(btn_frame, 
                           text="Adicionar",
                           style="TButton")
        add_btn.pack(side="left", padx=5)

        transaction_btn = ttk.Button(btn_frame, 
                                   text="Transação",
                                   style="TButton")
        transaction_btn.pack(side="left", padx=5)

        # Métricas do mês
        metrics_title = ttk.Label(inner_frame, 
                                text="Métricas do mês",
                                style="TLabel")
        metrics_title.pack(pady=(10, 5))

        # Checkboxes (simulando tarefas)
        tk.Checkbutton(inner_frame, 
                     text="", 
                     bg=self.color_palette["white"]).pack(anchor="w", pady=5)
        tk.Checkbutton(inner_frame, 
                     text="", 
                     bg=self.color_palette["white"]).pack(anchor="w", pady=5)