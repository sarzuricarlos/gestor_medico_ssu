import customtkinter as ctk

from src.vistas.tarjeta_medicamento import TarjetaMedicamento

COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")


class FrameConsultaMedicamentos(ctk.CTkFrame):
    """Pantalla de consulta de medicamentos con barra de búsqueda y tarjetas (HU-02)."""

    def __init__(self, master, app, repositorio=None):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.repositorio = repositorio

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._crear_encabezado()
        self._crear_barra_busqueda()
        self._crear_panel_resultados()

        self.mostrar_resultados([])

    def _crear_encabezado(self):
        ctk.CTkLabel(
            self,
            text="Consulta de Medicamentos",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        ctk.CTkLabel(
            self,
            text="Busque un medicamento por su nombre para ver disponibilidad y stock.",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).grid(row=0, column=0, sticky="w", pady=(36, 12))

    def _crear_barra_busqueda(self):
        frame_busqueda = ctk.CTkFrame(self, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        frame_busqueda.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        frame_busqueda.grid_columnconfigure(0, weight=1)

        self.entrada_busqueda = ctk.CTkEntry(
            frame_busqueda,
            placeholder_text="Nombre del medicamento...",
            height=40,
            font=ctk.CTkFont(size=14),
        )
        self.entrada_busqueda.grid(row=0, column=0, sticky="ew", padx=(16, 8), pady=16)

        ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            height=40,
            command=self.buscar_medicamentos,
        ).grid(row=0, column=1, padx=(0, 16), pady=16)

        self.entrada_busqueda.bind("<Return>", lambda _: self.buscar_medicamentos())

    def _crear_panel_resultados(self):
        self.panel_resultados = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.panel_resultados.grid(row=2, column=0, sticky="nsew")
        self.panel_resultados.grid_columnconfigure((0, 1, 2), weight=1, uniform="tarjeta")

    def buscar_medicamentos(self):
        """Busca medicamentos por nombre y actualiza las tarjetas."""
        nombre = self.entrada_busqueda.get().strip()

        if self.repositorio is None:
            self.mostrar_resultados([])
            return

        try:
            if nombre:
                resultados = self.repositorio.buscar_medicamentos_por_nombre(nombre)
            else:
                resultados = self.repositorio.obtener_todos_medicamentos()
        except Exception as e:
            print(f"Error al buscar medicamentos: {e}")
            resultados = []

        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, lista_medicamentos):
        """Limpia el panel y dibuja una tarjeta por cada medicamento."""
        for widget in self.panel_resultados.winfo_children():
            widget.destroy()

        if not lista_medicamentos:
            ctk.CTkLabel(
                self.panel_resultados,
                text="No se encontraron medicamentos.",
                font=ctk.CTkFont(size=14),
                text_color=COLOR_TEXTO_SECUNDARIO,
            ).grid(row=0, column=0, columnspan=3, pady=40)
            return

        columnas = 3
        for indice, medicamento in enumerate(lista_medicamentos):
            tarjeta = TarjetaMedicamento(self.panel_resultados, medicamento)
            tarjeta.grid(
                row=indice // columnas,
                column=indice % columnas,
                sticky="nsew",
                padx=8,
                pady=8,
            )