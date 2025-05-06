import tkinter as tk
from tkinter import ttk

class BalanceFrame(tk.Frame):
    def __init__(self, parent, color_palette):
        super().__init__(parent, bg=color_palette["light_gray"], padx=10, pady=10)
        self.color_palette = color_palette
        self.create_widgets()

    def create_widgets(self):
        # Frame interno para borda
        inner_frame = tk.Frame(self, bg=self.color_palette["white"], padx=20, pady=20)
        inner_frame.pack(expand=True, fill="both")

        # Título
        title = ttk.Label(inner_frame, 
                        text="Your balance",
                        style="TLabel")
        title.pack(pady=(0, 10))

        # Valor do saldo
        balance_value = ttk.Label(inner_frame, 
                                text="R$ 1.200,00",
                                font=("Segoe UI", 24, "bold"),
                                foreground=self.color_palette["dark_blue"])
        balance_value.pack()