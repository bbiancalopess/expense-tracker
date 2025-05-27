import locale
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from src.services.transaction_service import TransactionService
from utils import date


class MetricsWindow(tk.Frame):
    def __init__(self, master, color_palette):
        super().__init__(master, bg=color_palette["light_gray"])
        self.color_palette = color_palette
        self.selected_view = tk.StringVar(value="categoria")
        self.transaction_service = TransactionService()
        self.figures = []
        self.create_widgets()

        self.bind("<Destroy>", self.on_destroy)

    def on_destroy(self, event):
        """Fecha todos os recursos gráficos quando o frame for destruído"""

        for fig in self.figures:
            plt.close(fig)

        self.figures.clear()

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

        self.on_destroy(None)
        self.populate_metrics(self.selected_view.get())

    def populate_metrics(self, modo):
        if modo == "categoria":
            # Obter dados para visualização por categoria
            expenses_per_category = (
                self.transaction_service.find_expenses_per_category_for_current_month()
            )
            total_expense = (
                self.transaction_service.find_total_expense_for_current_month()
            )
            most_used_category = (
                self.transaction_service.find_most_used_category_for_current_month()
            )
            monthly_transactions = self.transaction_service.count_transactions()

            dados = [
                ("Total Gasto:", f"R$ {total_expense:.2f}"),
                ("Categoria mais frequente:", most_used_category),
                ("Transações no mês:", monthly_transactions),
            ]

            # Criar gráfico de pizza com os dados reais
            grafico = self.criar_grafico_pizza(expenses_per_category)

        elif modo == "mes":
            # Obter dados para visualização por mês (você precisará implementar isso no service)
            monthly_data = self.transaction_service.get_monthly_expenses()
            total_current = monthly_data[-1]["total"] if monthly_data else 0.0
            total_previous = monthly_data[-2]["total"] if len(monthly_data) > 1 else 0.0
            average = (
                sum(item["total"] for item in monthly_data) / len(monthly_data)
                if monthly_data
                else 0
            )

            current_month_en = datetime.now().strftime("%B").capitalize()
            previous_month_en = (
                datetime.now().replace(day=1) - timedelta(days=1)
            ).strftime("%B").capitalize()

            current_month_name = date.month_translation[current_month_en]
            previous_month_name = date.month_translation[previous_month_en]

            dados = [
                (f"Total em {current_month_name}:", f"R$ {total_current:.2f}"),
                (f"Total em {previous_month_name}:", f"R$ {total_previous:.2f}"),
                ("Média mensal:", f"R$ {average:.2f}"),
            ]

            # Criar gráfico de linha com os dados reais
            grafico = self.criar_grafico_linha(monthly_data)

        # Exibir métricas
        for label, valor in dados:
            row = ttk.Frame(self.metrics_frame)
            row.pack(anchor="w", pady=5)
            ttk.Label(row, text=label, style="TLabel").pack(side="left", padx=(0, 10))
            ttk.Label(row, text=valor, style="TLabel").pack(side="left")

        # Exibir gráfico
        canvas = FigureCanvasTkAgg(grafico, master=self.metrics_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def criar_grafico_pizza(self, data):
        if not data:
            # Retorna um gráfico vazio se não houver dados
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.text(0.5, 0.5, "Sem dados disponíveis", ha="center", va="center")
            ax.axis("off")
            self.figures.append(fig)
            return fig

        categories = []
        values = []
        for item in data:
            categories.append(item["name"])
            values.append(item["total_expense"])

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(values, labels=categories, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        self.figures.append(fig)
        return fig

    def criar_grafico_linha(self, monthly_data):
        if not monthly_data:
            # Retorna um gráfico vazio se não houver dados
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.text(0.5, 0.5, "Sem dados disponíveis", ha="center", va="center")
            ax.axis("off")
            self.figures.append(fig)
            return fig

        months = [item["month"] for item in monthly_data]
        values = [item["total"] for item in monthly_data]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(months, values, marker="o", color="teal")
        ax.set_title("Gastos Mensais")
        ax.set_ylabel("Valor (R$)")
        ax.grid(True)

        # Rotacionar labels dos meses para melhor visualização
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.figures.append(fig)
        return fig
