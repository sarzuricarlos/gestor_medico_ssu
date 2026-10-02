import customtkinter as ctk

# Colores en formato (modo claro, modo oscuro), iguales a los de app_seguro.py
COLOR_PRIMARIO = ("#1F6AA5", "#1A4F7A")
COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")
COLOR_TEXTO_ENCABEZADO = "#FFFFFF"

TEXTO_SIN_DATOS = "—"

COLOR_BANNER_HABILITADO = "#2E7D32"
COLOR_BANNER_INHABILITADO = "#C62828"
COLOR_BANNER_SIN_DATOS = "#7F8C8D"
TEXTO_BANNER_HABILITADO = "SU SEGURO SE ENCUENTRA HABILITADO"
TEXTO_BANNER_INHABILITADO = "SU SEGURO SE ENCUENTRA INHABILITADO"

# (atributo del label, título del indicador, color del distintivo)
INDICADORES = (
    ("lbl_estado_seguro", "Estado del seguro", "#F39C12"),
    ("lbl_aportes_vigentes", "Aportes vigentes", "#10AC84"),
    ("lbl_requisito_pendiente", "Requisito pendiente", "#E74C3C"),
)


class FrameEstadoSeguroDocente(ctk.CTkFrame):
    """Panel informativo para que el docente consulte el estado de su seguro (HU-03)."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.crear_encabezado()
        self.crear_perfil()
        self.crear_titulo_indicadores()
        self.crear_indicadores()

    def crear_encabezado(self):
        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            encabezado,
            text="Estado del Seguro Docente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLOR_TEXTO,
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Consulte la habilitación de su seguro y los requisitos pendientes",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        self.crear_banner_estado(encabezado)

    def crear_banner_estado(self, master):
        """Crea el label destacado que indica si el seguro esta habilitado."""
        self.banner_estado = ctk.CTkLabel(
            master,
            text=TEXTO_SIN_DATOS,
            height=64,
            corner_radius=14,
            fg_color=COLOR_BANNER_SIN_DATOS,
            text_color=COLOR_TEXTO_ENCABEZADO,
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.banner_estado.pack(fill="x", pady=(12, 0))

    def actualizar_banner_estado(self, estado_seguro):
        """Muestra el banner verde o rojo segun estado_seguro ('HABILITADO' o 'INHABILITADO')."""
        # Verde si esta habilitado, rojo si esta inhabilitado
        if estado_seguro == "HABILITADO":
            self.banner_estado.configure(
                text=TEXTO_BANNER_HABILITADO, fg_color=COLOR_BANNER_HABILITADO
            )
        elif estado_seguro == "INHABILITADO":
            self.banner_estado.configure(
                text=TEXTO_BANNER_INHABILITADO, fg_color=COLOR_BANNER_INHABILITADO
            )
        else:
            self.banner_estado.configure(
                text=TEXTO_SIN_DATOS, fg_color=COLOR_BANNER_SIN_DATOS
            )

    def crear_perfil(self):
        perfil = ctk.CTkFrame(self, fg_color=COLOR_PRIMARIO, corner_radius=14)
        perfil.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        perfil.grid_columnconfigure(1, weight=1)

        self.lbl_inicial = ctk.CTkLabel(
            perfil,
            text="D",
            width=64,
            height=64,
            corner_radius=32,
            fg_color=COLOR_TEXTO_ENCABEZADO,
            text_color=COLOR_PRIMARIO,
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.lbl_inicial.grid(row=0, column=0, rowspan=2, padx=(24, 16), pady=20)

        self.lbl_nombre = ctk.CTkLabel(
            perfil,
            text=TEXTO_SIN_DATOS,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
            anchor="w",
        )
        self.lbl_nombre.grid(row=0, column=1, sticky="sw", pady=(20, 0))

        self.lbl_rol = ctk.CTkLabel(
            perfil,
            text="DOCENTE",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXTO_ENCABEZADO,
            anchor="w",
        )
        self.lbl_rol.grid(row=1, column=1, sticky="nw", pady=(0, 20))

        self.lbl_id_usuario = ctk.CTkLabel(
            perfil,
            text=f"ID usuario: {TEXTO_SIN_DATOS}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        )
        self.lbl_id_usuario.grid(row=0, column=2, rowspan=2, padx=24)

    def crear_titulo_indicadores(self):
        ctk.CTkLabel(
            self,
            text="Indicadores del seguro",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=2, column=0, sticky="w", pady=(0, 10))

    def crear_indicadores(self):
        cuadricula = ctk.CTkFrame(self, fg_color="transparent")
        cuadricula.grid(row=3, column=0, sticky="new")

        for columna, (atributo, titulo, color) in enumerate(INDICADORES):
            cuadricula.grid_columnconfigure(columna, weight=1, uniform="indicador")
            tarjeta, lbl_valor = self.crear_tarjeta_indicador(cuadricula, titulo, color)
            tarjeta.grid(row=0, column=columna, sticky="nsew", padx=8, pady=8)
            # Se guarda el label para poder mostrar los datos reales más adelante
            setattr(self, atributo, lbl_valor)

    def crear_tarjeta_indicador(self, master, titulo, color):
        tarjeta = ctk.CTkFrame(master, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        tarjeta.grid_columnconfigure(0, weight=1)

        ctk.CTkFrame(tarjeta, height=6, corner_radius=3, fg_color=color).grid(
            row=0, column=0, sticky="ew", padx=16, pady=(16, 12)
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=16)

        lbl_valor = ctk.CTkLabel(
            tarjeta,
            text=TEXTO_SIN_DATOS,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
            justify="left",
            wraplength=220,
        )
        lbl_valor.grid(row=2, column=0, sticky="w", padx=16, pady=(4, 16))

        return tarjeta, lbl_valor