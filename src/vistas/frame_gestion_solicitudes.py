from tkinter import ttk

# (clave del registro, encabezado visible, ancho)
COLUMNAS = (
    ("id_solicitud_medica", "ID", 60),
    ("id_estudiante", "Estudiante", 90),
    ("nivel_urgencia", "Urgencia", 90),
    ("estado_solicitud", "Estado", 110),
    ("fecha_ingreso", "Fecha de ingreso", 150),
)


class FrameGestionSolicitudes(ttk.Frame):
    """Vista principal del panel de gestión de solicitudes (rol ENCARGADO)."""

    def __init__(self, master=None, repositorio=None, **kwargs):
        super().__init__(master, padding=12, **kwargs)
        self.repositorio = repositorio  # instancia de SolicitudRepository
        self._configurar_grid()
        self._crear_encabezado()
        self._crear_zona_filtros()
        self._crear_zona_tabla()

    def _configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)  # la tabla ocupa el espacio sobrante

    def _crear_encabezado(self):
        self.frame_encabezado = ttk.Frame(self)
        self.frame_encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.lbl_titulo = ttk.Label(
            self.frame_encabezado,
            text="Gestión de Solicitudes Médicas",
            font=("Segoe UI", 16, "bold"),
        )
        self.lbl_titulo.pack(anchor="w")

        self.lbl_subtitulo = ttk.Label(
            self.frame_encabezado,
            text="Panel del encargado · revise, filtre y dictamine solicitudes",
        )
        self.lbl_subtitulo.pack(anchor="w")

    def _crear_zona_filtros(self):
        self.frame_filtros = ttk.LabelFrame(self, text="Filtros", padding=8)
        self.frame_filtros.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    def _crear_zona_tabla(self):
        self.frame_tabla = ttk.LabelFrame(self, text="Solicitudes", padding=8)
        self.frame_tabla.grid(row=2, column=0, sticky="nsew")
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=[c[0] for c in COLUMNAS],
            show="headings",
            selectmode="browse",
        )
        for clave, titulo, ancho in COLUMNAS:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, anchor="w")

        scroll = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

    def cargar_tabla_solicitudes(self):
        """Limpia las filas actuales y muestra las solicitudes del repositorio."""
        self.tabla.delete(*self.tabla.get_children())
        if self.repositorio is None:
            return
        for fila in self.repositorio.listar_solicitudes():
            if isinstance(fila, dict):  # si no, se espera una tupla en el orden de COLUMNAS
                fila = [fila[clave] for clave, _, _ in COLUMNAS]
            self.tabla.insert("", "end", values=fila)
