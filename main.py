"""
Punto de entrada del sistema Gestor Médico SSU.
Ejecuta la aplicación completa.
"""
from src.creacionbd import CreacionBaseDatos
from src.conexion import ConexionBaseDatos
from src.app_seguro import AppSeguro


def main():
    # Inicializar la base de datos (crea tablas y datos iniciales)
    try:
        CreacionBaseDatos.inicializar_bd()
    except Exception as e:
        print(f"Advertencia: no se pudo inicializar la BD: {e}")

    # Iniciar la aplicación gráfica
    try:
        app = AppSeguro()
        app.mainloop()
    finally:
        ConexionBaseDatos.cerrar_conexion()


if __name__ == "__main__":
    main()