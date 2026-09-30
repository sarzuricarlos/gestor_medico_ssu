import customtkinter as ctk

COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")
COLOR_TEXTO_ENCABEZADO = "#FFFFFF"

COLOR_HABILITADO = "#10AC84"
COLOR_INHABILITADO = "#E74C3C"


class FrameEstadoSeguroDocente(ctk.CTkFrame):
    """Panel informativo del estado del seguro para docentes (HU-03)."""

    def __init__(self, master, app, repositorio=None):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.repositorio = repositorio

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._crear_encabezado()
        self._crear_banner_estado()
        self._crear_seccion_informativa()

    def _crear_encabezado(self):
        ctk.CTkLabel(
            self,
            text="Estado del Seguro Docente",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, sticky="w", pady=(0, 16))

    def _crear_banner_estado(self):
        """Banner dinámico que cambia de color según el estado del seguro."""
        self.frame_banner = ctk.CTkFrame(self, corner_radius=12, height=90)
        self.frame_banner.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.frame_banner.grid_propagate(False)

        self.label_banner = ctk.CTkLabel(
            self.frame_banner,
            text="",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        )
        self.label_banner.pack(expand=True)

    def _crear_seccion_informativa(self):
        self.frame_info = ctk.CTkFrame(self, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        self.frame_info.grid(row=2, column=0, sticky="nsew")
        self.frame_info.grid_columnconfigure(0, weight=1)

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
        self.texto_requisitos.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.texto_requisitos.configure(state="disabled")

    def cargar_estado(self, id_usuario):
        """Consulta el estado del seguro y actualiza la vista."""
        if self.repositorio is None:
            self._actualizar_vista(None)
            return

        try:
            estado = self.repositorio.obtener_estado_seguro_docente(id_usuario)
        except Exception as e:
            print(f"Error al consultar estado del seguro: {e}")
            estado = None

        self._actualizar_vista(estado)

    def _actualizar_vista(self, estado):
        if not estado:
            self.frame_banner.configure(fg_color="gray40")
            self.label_banner.configure(text="SIN INFORMACIÓN DISPONIBLE")
            self.label_aportes.configure(text="No se encontró información del seguro.")
            self._set_texto_requisitos("Sin datos.")
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

        aportes = "Aportes al día" if estado.get("aportes_vigentes") else "Aportes pendientes / irregulares"
        self.label_aportes.configure(text=f"Estado de aportes: {aportes}")

        requisitos = estado.get("requisito_pendiente") or "No tiene trámites pendientes."
        self._set_texto_requisitos(requisitos)

    def _set_texto_requisitos(self, texto):
        self.texto_requisitos.configure(state="normal")
        self.texto_requisitos.delete("1.0", "end")
        self.texto_requisitos.insert("1.0", texto)
        self.texto_requisitos.configure(state="disabled")