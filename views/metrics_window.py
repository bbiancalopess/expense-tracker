import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


class MetricsWindow(tk.Frame):
    def __init__(self, master, color_palette):
        super().__init__(master, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.selected_view = tk.StringVar(value="categoria")
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.color_palette["light_gray"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(
            main_frame, bg=self.color_palette["white"], padx=20, pady=15
        )
        header_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            header_frame,
            text="Métricas",
            style="Title.TLabel",
            background=self.color_palette["white"],
        ).pack(anchor="w")

        # Botões de alternância
        toggle_frame = tk.Frame(header_frame, bg=self.color_palette["white"])
        toggle_frame.pack(anchor="w", pady=(10, 0))

        ttk.Radiobutton(
            toggle_frame,
            text="Por Categoria",
            variable=self.selected_view,
            value="categoria",
            style="TRadiobutton",
            command=self.update_view,
        ).pack(side="left", padx=5)
        ttk.Radiobutton(
            toggle_frame,
            text="Por Mês",
            variable=self.selected_view,
            value="mes",
            style="TRadiobutton",
            command=self.update_view,
        ).pack(side="left", padx=5)

        # Área de métricas
        self.metrics_frame = tk.Frame(
            main_frame, bg=self.color_palette["white"], padx=20, pady=15
        )
        self.metrics_frame.pack(fill="both", expand=True)

        self.populate_metrics("categoria")

    def update_view(self):
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        self.populate_metrics(self.selected_view.get())

    def populate_metrics(self, modo):
        if modo == "categoria":
            dados = [
                ("Total Gasto:", "R$ 1.250,00"),
                ("Categoria mais frequente:", "Alimentação"),
                ("Transações no mês:", "18"),
            ]
            grafico = self.criar_grafico_pizza()
        elif modo == "mes":
            dados = [
                ("Total em Maio:", "R$ 900,00"),
                ("Total em Abril:", "R$ 1.050,00"),
                ("Média mensal:", "R$ 975,00"),
            ]
            grafico = self.criar_grafico_linha()

        for label, valor in dados:
            row = ttk.Frame(self.metrics_frame)
            row.pack(anchor="w", pady=5)
            ttk.Label(row, text=label, style="TLabel").pack(side="left", padx=(0, 10))
            ttk.Label(row, text=valor, style="TLabel").pack(side="left")

        canvas = FigureCanvasTkAgg(grafico, master=self.metrics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def criar_grafico_pizza(self):
        categorias = ["Alimentação", "Transporte", "Lazer", "Educação"]
        valores = [500, 300, 200, 250]

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        return fig

    def criar_grafico_linha(self):
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai"]
        valores = [800, 950, 1100, 1050, 900]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(meses, valores, marker="o", color="teal")
        ax.set_title("Gastos por Mês")
        ax.set_ylabel("Valor (R$)")
        ax.grid(True)
        return fig
