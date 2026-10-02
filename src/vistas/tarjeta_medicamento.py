import customtkinter as ctk

# Colores en formato (modo claro, modo oscuro), iguales a los de app_seguro.py
COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")
COLOR_TEXTO_ENCABEZADO = "#FFFFFF"

COLOR_DISPONIBLE = "green"
COLOR_SIN_STOCK = "red"
TEXTO_SIN_DESCRIPCION = "Sin descripción"


class TarjetaMedicamento(ctk.CTkFrame):
    """Tarjeta que muestra un medicamento con una etiqueta de color según su stock (HU-02)."""

    def __init__(self, master, medicamento):
        super().__init__(master, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        self.medicamento = medicamento  # diccionario devuelto por la consulta SQL

        self.grid_columnconfigure(0, weight=1)

        self.crear_nombre()
        self.crear_descripcion()
        self.crear_etiqueta_estado()

    def crear_nombre(self):
        ctk.CTkLabel(
            self,
            text=self.medicamento["nombre_medicamento"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 2))

    def crear_descripcion(self):
        descripcion = self.medicamento.get("descripcion_medicamento") or TEXTO_SIN_DESCRIPCION
        ctk.CTkLabel(
            self,
            text=descripcion,
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w",
            justify="left",
            wraplength=240,
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 10))

    def crear_etiqueta_estado(self):
        stock = self.medicamento["stock_medicamento"]
        if stock > 0:
            texto, color = f"Disponible (Stock: {stock})", COLOR_DISPONIBLE
        else:
            texto, color = "Sin Stock", COLOR_SIN_STOCK

        ctk.CTkLabel(
            self,
            text=texto,
            fg_color=color,
            text_color=COLOR_TEXTO_ENCABEZADO,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
        ).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 16), ipadx=8)
