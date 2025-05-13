import tkinter as tk
from tkinter import ttk

class MetricsWindow(tk.Frame):
    def __init__(self, master, color_palette):
        super().__init__(master, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.create_widgets()

    def create_widgets(self):
        # Título
        title = ttk.Label(self, text="Métricas", style="Title.TLabel")
        title.pack(anchor="w", pady=(0, 20))

        # Exemplo de conteúdo
        metrics_info = [
            ("Total Gasto:", "R$ 1.250,00"),
            ("Categoria mais frequente:", "Alimentação"),
            ("Transações no mês:", "18"),
        ]

        for label, value in metrics_info:
            row = ttk.Frame(self)
            row.pack(anchor="w", pady=5)

            ttk.Label(row, text=label, style="TLabel").pack(side="left", padx=(0, 10))
            ttk.Label(row, text=value, style="TLabel").pack(side="left")

        # Espaço reservado para futuros gráficos ou análises
        placeholder = tk.Label(self,
            text="Gráficos de pizza e linha serão exibidos aqui futuramente.",
            bg=self.color_palette["light_gray"],
            fg=self.color_palette["dark_blue"],
            font=("Segoe UI", 10, "italic"),
            pady=40)
        placeholder.pack(anchor="center", expand=True)
