import customtkinter as ctk

# Colores en formato (modo claro, modo oscuro), iguales a los de app_seguro.py
COLOR_PRIMARIO = ("#1F6AA5", "#1A4F7A")
COLOR_FONDO = ("#EEF2F7", "#16181C")
COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_ENCABEZADO = "#FFFFFF"

ANCHO_VENTANA = 520
ALTO_VENTANA = 460


class VentanaDictamenModal(ctk.CTkToplevel):
    """Ventana emergente para dictaminar la solicitud seleccionada en el Treeview (HU-01)."""

    def __init__(self, master, id_solicitud):
        super().__init__(master)
        self.id_solicitud = id_solicitud

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.configurar_ventana()
        self.crear_encabezado()
        self.crear_cuerpo()
        self.crear_botones()
        # Se espera a que la ventana sea visible antes de bloquear la principal
        self.after(100, self.activar_modo_modal)

    def configurar_ventana(self):
        self.title(f"Dictamen de solicitud #{self.id_solicitud}")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_FONDO)
        self.transient(self.master.winfo_toplevel())
        self.centrar_sobre_ventana_principal()

    def centrar_sobre_ventana_principal(self):
        principal = self.master.winfo_toplevel()
        principal.update_idletasks()
        x = principal.winfo_rootx() + (principal.winfo_width() - ANCHO_VENTANA) // 2
        y = principal.winfo_rooty() + (principal.winfo_height() - ALTO_VENTANA) // 2
        self.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}+{max(x, 0)}+{max(y, 0)}")

    def activar_modo_modal(self):
        """Bloquea la ventana principal mientras el modal esté abierto."""
        self.grab_set()
        self.focus_force()

    def crear_encabezado(self):
        encabezado = ctk.CTkFrame(self, fg_color=COLOR_PRIMARIO, corner_radius=0)
        encabezado.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            encabezado,
            text="Dictaminar solicitud médica",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO_ENCABEZADO,
        ).pack(anchor="w", padx=20, pady=(16, 0))

        ctk.CTkLabel(
            encabezado,
            text=f"Solicitud N.º {self.id_solicitud}",
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXTO_ENCABEZADO,
        ).pack(anchor="w", padx=20, pady=(0, 16))

    def crear_cuerpo(self):
        # Contenedor donde irá el formulario del dictamen
        self.frame_formulario = ctk.CTkFrame(self, fg_color=COLOR_SUPERFICIE, corner_radius=12)
        self.frame_formulario.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_formulario.grid_columnconfigure(0, weight=1)

    def crear_botones(self):
        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.grid(row=2, column=0, sticky="e", padx=20, pady=(0, 20))

        self.btn_cancelar = ctk.CTkButton(
            botones,
            text="Cancelar",
            width=110,
            fg_color="transparent",
            border_width=1,
            text_color=COLOR_TEXTO,
            command=self.cerrar,
        )
        self.btn_cancelar.pack(side="right")

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def cerrar(self):
        self.grab_release()
        self.destroy()
