import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from src.sesion import SesionUsuario
from src.solicitudes import actualizar_dictamen_solicitud
from src.notificaciones import Notificaciones

COLOR_SUPERFICIE = ("#FFFFFF", "#212429")
COLOR_TEXTO = ("#1C2733", "#E6E9EE")
COLOR_TEXTO_SECUNDARIO = ("#5B6B7C", "#9AA5B1")


class VentanaDictamenModal(ctk.CTkToplevel):
    """Ventana modal para dictaminar una solicitud médica (HU-01)."""

    def __init__(self, master, id_solicitud, al_guardar=None):
        super().__init__(master)
        self.id_solicitud = id_solicitud
        self.al_guardar = al_guardar  # callback para refrescar la tabla principal

        self.title(f"Dictamen de Solicitud #{id_solicitud}")
        self.geometry("460x480")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_SUPERFICIE)

        # Hacer el modal bloqueante
        self.transient(master)
        self.grab_set()

        self.estado_var = tk.StringVar(value="APROBADO")
        self._crear_widgets()

    def _crear_widgets(self):
        # Título
        ctk.CTkLabel(
            self,
            text=f"Solicitud #{self.id_solicitud}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXTO,
        ).pack(pady=(20, 4), padx=20, anchor="w")

        ctk.CTkLabel(
            self,
            text="Seleccione el estado y escriba una justificación obligatoria.",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).pack(pady=(0, 16), padx=20, anchor="w")

        # Radio buttons
        frame_radios = ctk.CTkFrame(self, fg_color="transparent")
        frame_radios.pack(padx=20, pady=(0, 12), fill="x")

        for opcion in ("APROBADO", "RECHAZADO", "OBSERVADO"):
            ctk.CTkRadioButton(
                frame_radios,
                text=opcion.capitalize(),
                variable=self.estado_var,
                value=opcion,
                font=ctk.CTkFont(size=14),
            ).pack(anchor="w", pady=4)

        # Caja de texto para justificación
        ctk.CTkLabel(
            self,
            text="Justificación:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_TEXTO,
        ).pack(padx=20, anchor="w")

        self.texto_justificacion = ctk.CTkTextbox(
            self, height=140, font=ctk.CTkFont(size=13)
        )
        self.texto_justificacion.pack(padx=20, pady=(4, 16), fill="x")

        # Botones
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkButton(
            frame_botones, text="Cancelar", fg_color="gray40",
            command=self.destroy,
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            frame_botones, text="Guardar dictamen", command=self.validar_y_guardar,
        ).pack(side="right")

    def validar_y_guardar(self):
        """Valida que la justificación no esté vacía y guarda el dictamen."""
        justificacion = self.texto_justificacion.get("1.0", "end").strip()

        if not justificacion:
            messagebox.showerror(
                "Justificación requerida",
                "Debe ingresar una justificación antes de guardar el dictamen.",
                parent=self,
            )
            return

        estado = self.estado_var.get()
        id_operador = SesionUsuario.obtener_id_usuario()

        try:
            actualizado = actualizar_dictamen_solicitud(
                self.id_solicitud, estado, justificacion, id_operador
            )

            if not actualizado:
                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró la solicitud indicada.",
                    parent=self,
                )
                return

            # Crear notificación automática para el estudiante
            mensaje = f"Su solicitud #{self.id_solicitud} fue {estado.lower()}."
            try:
                Notificaciones.crear_notificacion_estudiante(
                    self.id_solicitud, self.id_solicitud, mensaje
                )
            except Exception as e:
                print(f"Advertencia: no se pudo crear la notificación: {e}")

            messagebox.showinfo(
                "Dictamen guardado",
                f"La solicitud #{self.id_solicitud} fue {estado.lower()} correctamente.",
                parent=self,
            )

            if self.al_guardar:
                self.al_guardar()

            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el dictamen:\n{e}", parent=self)