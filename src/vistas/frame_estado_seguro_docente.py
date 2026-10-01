import customtkinter as ctk

from src.sesion import SesionUsuario

COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")
COLOR_TEXTO_ENCABEZADO = "#FFFFFF"

COLOR_HABILITADO = "#10AC84"
COLOR_INHABILITADO = "#E74C3C"
COLOR_NEUTRO = "gray40"

# Texto especial para el selector que permite buscar al docente en sesión
OPCION_SESION = "▶ Usuario en sesión"


class FrameEstadoSeguroDocente(ctk.CTkFrame):
    """Panel informativo del estado del seguro para docentes (HU-03).

    Incluye un selector para cambiar entre todos los docentes registrados.
    """

    def __init__(self, master, app, repositorio=None):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.repositorio = repositorio

        # Mapa nombre_visible -> id_usuario
        self.mapa_docentes = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._crear_encabezado()
        self._crear_selector_docente()
        self._crear_banner_estado()
        self._crear_seccion_informativa()

        # Cargar docentes y mostrar el primero (o el de sesión)
        self._cargar_lista_docentes()
        self._seleccionar_docente_inicial()

    # ------------------------------------------------------------------ #
    #  Construcción de la interfaz
    # ------------------------------------------------------------------ #

    def _crear_encabezado(self):
        ctk.CTkLabel(
            self,
            text="Estado del Seguro Docente",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        ctk.CTkLabel(
            self,
            text="Seleccione un docente para consultar su estado de seguro y aportes.",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).grid(row=0, column=0, sticky="w", pady=(60, 12))

    def _crear_selector_docente(self):
        """Barra con el selector de docentes."""
        frame_selector = ctk.CTkFrame(self, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        frame_selector.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        frame_selector.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            frame_selector,
            text="Docente:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, padx=(16, 8), pady=14, sticky="w")

        self.selector_docente = ctk.CTkOptionMenu(
            frame_selector,
            values=["Cargando..."],
            command=self._on_docente_seleccionado,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            height=36,
            dynamic_resizing=False,
        )
        self.selector_docente.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=14)

    def _crear_banner_estado(self):
        """Banner dinámico que cambia de color según el estado del seguro."""
        self.frame_banner = ctk.CTkFrame(self, corner_radius=12, height=90, fg_color=COLOR_NEUTRO)
        self.frame_banner.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.frame_banner.grid_propagate(False)

        self.label_banner = ctk.CTkLabel(
            self.frame_banner,
            text="SELECCIONE UN DOCENTE",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        )
        self.label_banner.pack(expand=True)

    def _crear_seccion_informativa(self):
        self.frame_info = ctk.CTkFrame(self, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        self.frame_info.grid(row=3, column=0, sticky="nsew")
        self.frame_info.grid_columnconfigure(0, weight=1)
        self.frame_info.grid_rowconfigure(2, weight=1)

        self.label_aportes = ctk.CTkLabel(
            self.frame_info,
            text="",
            font=ctk.CTkFont(size=15),
            text_color=COLOR_TEXTO,
            anchor="w",
        )
        self.label_aportes.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 8))

        ctk.CTkLabel(
            self.frame_info,
            text="Requisitos y trámites pendientes:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(12, 4))

        self.texto_requisitos = ctk.CTkTextbox(
            self.frame_info, height=160, font=ctk.CTkFont(size=13)
        )
        self.texto_requisitos.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.texto_requisitos.configure(state="disabled")

    # ------------------------------------------------------------------ #
    #  Carga y lógica
    # ------------------------------------------------------------------ #

    def _cargar_lista_docentes(self):
        """Carga todos los docentes desde el repositorio y llena el selector."""
        if self.repositorio is None:
            self.selector_docente.configure(values=["No disponible"])
            return

        try:
            docentes = self.repositorio.listar_docentes()
        except Exception as e:
            print(f"[EstadoSeguro] Error al listar docentes: {e}")
            docentes = []

        if not docentes:
            self.selector_docente.configure(values=["Sin docentes"])
            self.selector_docente.set("Sin docentes")
            return

        # Construir valores del menú: "ID - Nombre"
        valores = [OPCION_SESION]
        self.mapa_docentes = {}
        for id_doc, nombre in docentes:
            etiqueta = f"{id_doc} - {nombre}"
            valores.append(etiqueta)
            self.mapa_docentes[etiqueta] = id_doc

        self.selector_docente.configure(values=valores)

    def _seleccionar_docente_inicial(self):
        """Selecciona el docente en sesión si existe, si no el primero de la lista."""
        id_sesion = SesionUsuario.obtener_id_usuario()

        # Si hay sesión activa y es un docente, elegirlo
        if id_sesion is not None:
            for etiqueta, id_doc in self.mapa_docentes.items():
                if id_doc == id_sesion:
                    self.selector_docente.set(etiqueta)
                    self.cargar_estado(id_sesion)
                    return

        # Si no, tomar el primero disponible (excluyendo la opción de sesión)
        if self.mapa_docentes:
            primera_etiqueta = next(iter(self.mapa_docentes))
            self.selector_docente.set(primera_etiqueta)
            self.cargar_estado(self.mapa_docentes[primera_etiqueta])
        else:
            self._actualizar_vista(None)

    def _on_docente_seleccionado(self, etiqueta):
        """Callback cuando el usuario cambia de docente en el selector."""
        if etiqueta == OPCION_SESION:
            id_sesion = SesionUsuario.obtener_id_usuario()
            if id_sesion is not None:
                self.cargar_estado(id_sesion)
            else:
                self._actualizar_vista(None)
            return

        id_doc = self.mapa_docentes.get(etiqueta)
        if id_doc is not None:
            self.cargar_estado(id_doc)

    def cargar_estado(self, id_usuario):
        """Consulta el estado del seguro y actualiza la vista."""
        print(f"[EstadoSeguro] Consultando estado para id_usuario={id_usuario}")

        if self.repositorio is None:
            self._actualizar_vista(None)
            return

        try:
            estado = self.repositorio.obtener_estado_seguro_docente(id_usuario)
            print(f"[EstadoSeguro] Resultado: {estado}")
        except Exception as e:
            print(f"[EstadoSeguro] Error al consultar: {e}")
            estado = None

        self._actualizar_vista(estado, id_usuario)

    def _actualizar_vista(self, estado, id_usuario=None):
        """Actualiza el banner y la sección informativa con el estado recibido."""
        if not estado:
            self.frame_banner.configure(fg_color=COLOR_NEUTRO)
            self.label_banner.configure(text="SIN INFORMACIÓN DISPONIBLE")
            self.label_aportes.configure(
                text="No se encontró un registro de seguro para este docente."
            )
            self._set_texto_requisitos(
                "Verifique que exista un registro en la tabla 'docentes_seguros' "
                "para el id_usuario seleccionado."
            )
            return

        habilitado = estado.get("estado_seguro") == "HABILITADO"
        color = COLOR_HABILITADO if habilitado else COLOR_INHABILITADO
        texto = (
            "SU SEGURO SE ENCUENTRA HABILITADO"
            if habilitado
            else "SU SEGURO SE ENCUENTRA INHABILITADO"
        )

        self.frame_banner.configure(fg_color=color)
        self.label_banner.configure(text=texto)

        aportes = (
            "Aportes al día"
            if estado.get("aportes_vigentes")
            else "Aportes pendientes / irregulares"
        )
        encabezado = f"Estado de aportes: {aportes}"
        if id_usuario is not None:
            encabezado = f"Docente id={id_usuario}  ·  {encabezado}"
        self.label_aportes.configure(text=encabezado)

        requisitos = estado.get("requisito_pendiente") or "No tiene trámites pendientes."
        self._set_texto_requisitos(requisitos)

    def _set_texto_requisitos(self, texto):
        self.texto_requisitos.configure(state="normal")
        self.texto_requisitos.delete("1.0", "end")
        self.texto_requisitos.insert("1.0", texto)
        self.texto_requisitos.configure(state="disabled")