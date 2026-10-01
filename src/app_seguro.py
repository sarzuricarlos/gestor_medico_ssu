from datetime import datetime

import customtkinter as ctk

from src.sesion import SesionUsuario
from src.solicitudes import SolicitudRepository
from src.medicamentos import MedicamentoRepository
from src.docentes import DocenteRepository
from src.vistas.frame_gestion_solicitudes import FrameGestionSolicitudes
from src.vistas.frame_consulta_medicamentos import FrameConsultaMedicamentos
from src.vistas.frame_estado_seguro_docente import FrameEstadoSeguroDocente

TITULO_APP = "Gestor Médico - Seguro Social Universitario"
TAMANO_VENTANA = "1200x720"
TAMANO_MINIMO = (1100, 650)
VERSION_APP = "v0.1"

COLOR_PRIMARIO = ("#1F6AA5", "#1A4F7A")
COLOR_PRIMARIO_HOVER = ("#185A8C", "#16415F")
COLOR_FONDO = ("#EEF2F7", "#16181C")
COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")
COLOR_BOTON_MENU_HOVER = ("#DDE6F0", "#2B3038")
COLOR_TEXTO_ENCABEZADO = "#FFFFFF"

MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

MODULOS_SISTEMA = [
    ("S", "Solicitudes médicas", "Evaluación y gestión de solicitudes de atención.", "#2E86DE"),
    ("M", "Medicamentos", "Consulta de medicamentos disponibles y su stock.", "#10AC84"),
    ("E", "Estado del seguro", "Verificación de habilitación del seguro docente.", "#F39C12"),
    ("C", "Citas médicas", "Solicitud y consulta de citas con especialistas.", "#8E44AD"),
    ("A", "Afiliaciones", "Registro de afiliados y beneficiarios.", "#E74C3C"),
    ("R", "Reportes", "Reportes de uso del seguro universitario.", "#16A085"),
]


class VistaBienvenida(ctk.CTkFrame):
    """Pantalla inicial que se muestra al abrir la aplicación."""

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.crear_saludo()
        self.crear_titulo_modulos()
        self.crear_tarjetas_modulos()

    def crear_saludo(self):
        saludo = ctk.CTkFrame(self, fg_color=COLOR_PRIMARIO, corner_radius=14)
        saludo.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        saludo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            saludo,
            text=f"{self.obtener_saludo()}, bienvenido",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        ).grid(row=0, column=0, sticky="w", padx=28, pady=(24, 4))

        ctk.CTkLabel(
            saludo,
            text="Sistema de gestión médica del Seguro Social Universitario",
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXTO_ENCABEZADO,
        ).grid(row=1, column=0, sticky="w", padx=28, pady=(0, 24))

        ctk.CTkLabel(
            saludo,
            text=self.obtener_fecha(),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        ).grid(row=0, column=1, rowspan=2, padx=28)

    def crear_titulo_modulos(self):
        ctk.CTkLabel(
            self,
            text="Módulos del sistema",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

    def crear_tarjetas_modulos(self):
        cuadricula = ctk.CTkFrame(self, fg_color="transparent")
        cuadricula.grid(row=2, column=0, sticky="nsew")

        columnas = 3
        for columna in range(columnas):
            cuadricula.grid_columnconfigure(columna, weight=1, uniform="tarjeta")

        for indice, modulo in enumerate(MODULOS_SISTEMA):
            tarjeta = self.crear_tarjeta(cuadricula, *modulo)
            tarjeta.grid(row=indice // columnas, column=indice % columnas, sticky="nsew", padx=8, pady=8)

    def crear_tarjeta(self, master, inicial, titulo, descripcion, color):
        tarjeta = ctk.CTkFrame(master, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        tarjeta.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            tarjeta,
            text=inicial,
            width=44,
            height=44,
            corner_radius=10,
            fg_color=color,
            text_color=COLOR_TEXTO_ENCABEZADO,
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=16)

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_TEXTO,
            anchor="w",
        ).grid(row=0, column=1, sticky="sw", padx=(0, 16), pady=(16, 0))

        ctk.CTkLabel(
            tarjeta,
            text=descripcion,
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXTO_SECUNDARIO,
            anchor="w",
            justify="left",
            wraplength=170,
        ).grid(row=1, column=1, sticky="nw", padx=(0, 16), pady=(2, 16))

        return tarjeta

    def obtener_saludo(self):
        hora = datetime.now().hour
        if hora < 12:
            return "Buenos días"
        if hora < 19:
            return "Buenas tardes"
        return "Buenas noches"

    def obtener_fecha(self):
        hoy = datetime.now()
        return f"{hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"


class AppSeguro(ctk.CTk):
    """Ventana principal: encabezado, menú lateral y contenedor de vistas."""

    def __init__(self):
        super().__init__()
        self.vista_actual = None
        self.botones_menu = {}

        # Repositorios
        self.repo_solicitudes = SolicitudRepository()
        self.repo_medicamentos = MedicamentoRepository()
        self.repo_docentes = DocenteRepository()

        self.configurar_ventana()
        self.crear_encabezado()
        self.crear_menu_lateral()
        self.crear_contenedor()

        self.agregar_opcion_menu("Inicio", VistaBienvenida)

        # Vistas de las HU
        self.agregar_opcion_menu(
            "Solicitudes médicas",
            lambda master, app: FrameGestionSolicitudes(master, repositorio=self.repo_solicitudes),
        )
        self.agregar_opcion_menu(
            "Medicamentos",
            lambda master, app: FrameConsultaMedicamentos(master, app, repositorio=self.repo_medicamentos),
        )
        self.agregar_opcion_menu(
            "Estado del seguro",
            lambda master, app: FrameEstadoSeguroDocente(master, app, repositorio=self.repo_docentes),
        )

        self.mostrar_vista(VistaBienvenida)

    def configurar_ventana(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title(TITULO_APP)
        self.geometry(TAMANO_VENTANA)
        self.minsize(*TAMANO_MINIMO)
        self.configure(fg_color=COLOR_FONDO)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def crear_encabezado(self):
        encabezado = ctk.CTkFrame(self, height=64, corner_radius=0, fg_color=COLOR_PRIMARIO)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")
        encabezado.grid_propagate(False)
        encabezado.grid_rowconfigure(0, weight=1)
        encabezado.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="+",
            width=38,
            height=38,
            corner_radius=10,
            fg_color=COLOR_TEXTO_ENCABEZADO,
            text_color=COLOR_PRIMARIO,
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, padx=(20, 12))

        ctk.CTkLabel(
            encabezado,
            text="Gestor Médico SSU",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        ).grid(row=0, column=1, sticky="w")

        self.interruptor_tema = ctk.CTkSwitch(
            encabezado,
            text="Modo oscuro",
            text_color=COLOR_TEXTO_ENCABEZADO,
            font=ctk.CTkFont(size=13),
            progress_color="#0B2F4D",
            command=self.alternar_tema,
        )
        self.interruptor_tema.grid(row=0, column=2, padx=20)
        if ctk.get_appearance_mode() == "Dark":
            self.interruptor_tema.select()

    def crear_menu_lateral(self):
        self.menu_lateral = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_SUPERFICIE)
        self.menu_lateral.grid(row=1, column=0, sticky="ns")
        self.menu_lateral.grid_propagate(False)
        self.menu_lateral.grid_columnconfigure(0, weight=1)
        self.menu_lateral.grid_rowconfigure(99, weight=1)

        ctk.CTkLabel(
            self.menu_lateral,
            text="MENÚ",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self.menu_lateral,
            text=f"Seguro Social Universitario\n{VERSION_APP}",
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).grid(row=100, column=0, pady=20)

    def crear_contenedor(self):
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.grid(row=1, column=1, padx=24, pady=24, sticky="nsew")
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

    def agregar_opcion_menu(self, texto, clase_vista):
        boton = ctk.CTkButton(
            self.menu_lateral,
            text=texto,
            height=40,
            anchor="w",
            corner_radius=8,
            font=ctk.CTkFont(size=14),
            command=lambda: self.mostrar_vista(clase_vista),
        )
        boton.grid(row=len(self.botones_menu) + 1, column=0, sticky="ew", padx=12, pady=2)
        self.botones_menu[texto] = boton
        self.resaltar_opcion_menu()

    def resaltar_opcion_menu(self):
        for texto, boton in self.botones_menu.items():
            es_actual = self.vista_actual and texto == getattr(self, "_vista_actual_nombre", None)
            if es_actual:
                boton.configure(fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO_HOVER, text_color=COLOR_TEXTO_ENCABEZADO)
            else:
                boton.configure(fg_color="transparent", hover_color=COLOR_BOTON_MENU_HOVER, text_color=COLOR_TEXTO)

    def mostrar_vista(self, clase_vista, **kwargs):
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.vista_actual = clase_vista(self.contenedor, self, **kwargs)
        self.vista_actual.grid(row=0, column=0, sticky="nsew")
        self.resaltar_opcion_menu()
        return self.vista_actual

    def alternar_tema(self):
        if self.interruptor_tema.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")