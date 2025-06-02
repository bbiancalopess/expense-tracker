import tkinter as tk
from tkinter import ttk, messagebox
from src.services.category_service import CategoryService
from src.models.category import Category


class AddCategoryWindow(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.title("Adicionar Nova Categoria")
        self.geometry("400x300")
        self.callback = callback

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

        self.category_service = CategoryService()

        self.configure(bg=self.colors["light_gray"])
        self.create_widgets()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.colors["light_gray"], padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Título
        title_label = tk.Label(
            main_frame,
            text="Nova Categoria",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["light_gray"],
            fg=self.colors["dark_blue"],
            background=self.colors["light_gray"],
        )
        title_label.pack(pady=(0, 20))

        # Campo de entrada para o nome da categoria
        ttk.Label(
            main_frame,
            text="Nome da Categoria *",
            style="TLabel",
            background=self.colors["light_gray"],
        ).pack(
            anchor="w",
            pady=(0, 5),
        )
        self.category_entry = ttk.Entry(main_frame, font=("Segoe UI", 10))
        self.category_entry.pack(fill="x", pady=(0, 15))
        self.category_entry.focus()

        # Frame dos botões
        button_frame = tk.Frame(main_frame, bg=self.colors["light_gray"])
        button_frame.pack(fill="x", pady=(10, 0))

        # Botão Salvar
        save_button = ttk.Button(
            button_frame,
            text="Salvar",
            style="Blue.TButton",
            command=self.save_category,
        )
        save_button.pack(side="right", padx=5)

        # Botão Cancelar
        cancel_button = ttk.Button(
            button_frame,
            text="Cancelar",
            style="Red.TButton",
            command=self.destroy,
        )
        cancel_button.pack(side="right", padx=5)

    def save_category(self):
        """Valida e salva a nova categoria"""
        category_name = self.category_entry.get().strip()

        if not category_name:
            messagebox.showerror("Erro", "Por favor, informe o nome da categoria.")
            return

        # Aqui você pode adicionar a lógica para salvar a categoria no seu sistema
        new_category = self.category_service.add_category(Category(None, category_name))

        if self.callback:
            self.callback(new_category)
        messagebox.showinfo(
            "Sucesso", f"Categoria '{category_name}' adicionada com sucesso!"
        )
        self.destroy()
