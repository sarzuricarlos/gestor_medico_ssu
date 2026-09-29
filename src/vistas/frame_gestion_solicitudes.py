from tkinter import messagebox, ttk
import customtkinter as ctk
# (clave del registro, encabezado visible, ancho)
COLUMNAS = (
    ("id_solicitud_medica", "ID", 60),
    ("id_estudiante", "Estudiante", 90),
    ("fecha_ingreso", "Fecha", 150),
    ("nivel_urgencia", "Urgencia", 90),
    ("estado_solicitud", "Estado", 110),
)

OPCIONES_ESTADO = ("TODOS", "PENDIENTE", "APROBADO", "RECHAZADO", "OBSERVADO")
OPCIONES_URGENCIA = ("TODAS", "ALTA", "MEDIA", "BAJA")
# texto del menú -> clave de orden que entiende SolicitudRepository
OPCIONES_ORDEN = {
    "Urgencia: Mayor a Menor": "urgencia",
    "Fecha: Más Antiguas": "antiguas",
    "Fecha: Más Recientes": "recientes",
}

class FrameGestionSolicitudes(ttk.Frame):
    """Vista principal del panel de gestión de solicitudes (rol ENCARGADO)."""

    def __init__(self, master=None, repositorio=None, **kwargs):
        super().__init__(master, padding=12, **kwargs)
        self.repositorio = repositorio  # instancia de SolicitudRepository
        self._configurar_grid()
        self._crear_encabezado()
        self._crear_zona_filtros()
        self._crear_controles_filtros()
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

    def _crear_controles_filtros(self):
        """Coloca los controles de filtrado dentro de la zona de filtros."""
        self.combo_estado = ttk.Combobox(self.frame_filtros, values=OPCIONES_ESTADO, state="readonly", width=14)
        self.combo_urgencia = ttk.Combobox(self.frame_filtros, values=OPCIONES_URGENCIA, state="readonly", width=10)
        self.entry_estudiante = ttk.Entry(self.frame_filtros, width=14)
        self.combo_estado.set("PENDIENTE")
        self.combo_urgencia.set("TODAS")

        campos = (
            ("Estado:", self.combo_estado),
            ("Urgencia:", self.combo_urgencia),
            ("ID estudiante:", self.entry_estudiante),
        )
        for indice, (texto, control) in enumerate(campos):
            ttk.Label(self.frame_filtros, text=texto).grid(row=0, column=indice * 2, padx=(0 if indice == 0 else 12, 4))
            control.grid(row=0, column=indice * 2 + 1)

        # Columna vacía que empuja los botones hacia la derecha
        self.frame_filtros.columnconfigure(6, weight=1)

        self.btn_filtrar = ttk.Button(self.frame_filtros, text="Filtrar", command=self.aplicar_filtros)
        self.btn_filtrar.grid(row=0, column=7, padx=(12, 4))
        self.btn_limpiar = ttk.Button(self.frame_filtros, text="Limpiar", command=self.limpiar_filtros)
        self.btn_limpiar.grid(row=0, column=8)

        self.entry_estudiante.bind("<Return>", lambda _: self.aplicar_filtros())
        # Menú de ordenamiento: al elegir una opción se recarga la tabla
        ttk.Label(self.frame_filtros, text="Ordenar por:").grid(row=1, column=0, padx=(0, 4), pady=(8, 0), sticky="w")
        self.menu_orden = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=list(OPCIONES_ORDEN),
            command=lambda _valor: self.cargar_tabla_solicitudes(),
        )
        self.menu_orden.set("Fecha: Más Recientes")
        self.menu_orden.grid(row=1, column=1, columnspan=3, pady=(8, 0), sticky="w")

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
        estado = self.combo_estado.get()
        urgencia = self.combo_urgencia.get()
        id_estudiante = self.entry_estudiante.get().strip()

        if id_estudiante and not id_estudiante.isdigit():
            messagebox.showwarning("Filtro inválido", "El ID del estudiante debe ser un número.")
            return

        self.tabla.delete(*self.tabla.get_children())
        if self.repositorio is None:
            return

        orden = OPCIONES_ORDEN[self.menu_orden.get()]
        total = 0
        for fila in self.repositorio.listar_solicitudes(orden):
            if self._cumple_filtros(fila, estado, urgencia, id_estudiante):
                self.tabla.insert("", "end", values=[fila[clave] for clave, _, _ in COLUMNAS])
                total += 1
        self.frame_tabla.configure(text=f"Solicitudes ({total})")


    def cargar_solicitudes_pendientes(self):
        """Muestra en la tabla solo las solicitudes en estado PENDIENTE."""
        self.limpiar_filtros()
    def aplicar_filtros(self):
        """Muestra en la tabla solo las solicitudes que cumplen los filtros seleccionados."""
        self.limpiar_filtros()

    def limpiar_filtros(self):
        """Restablece los filtros a sus valores iniciales y recarga la tabla."""
        self.combo_estado.set("PENDIENTE")
        self.combo_urgencia.set("TODAS")
        self.entry_estudiante.delete(0, "end")
        self.cargar_tabla_solicitudes()

    def _cumple_filtros(self, fila, estado, urgencia, id_estudiante):
        if estado != "TODOS" and fila["estado_solicitud"] != estado:
            return False
        if urgencia != "TODAS" and fila["nivel_urgencia"] != urgencia:
            return False
        if id_estudiante and fila["id_estudiante"] != int(id_estudiante):
            return False
        return True
