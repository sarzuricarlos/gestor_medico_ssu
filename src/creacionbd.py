import sys
from pathlib import Path
from mysql.connector import Error

# Asegurar que Python reconozca la raíz del proyecto para importar conexion.py
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.conexion import ConexionBaseDatos


class CreacionBaseDatos:
    """Clase encargada de inicializar la estructura de la base de datos y cargar datos iniciales."""

    TABLAS = [
        # 1. Tabla Usuarios
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre_usuario VARCHAR(100) NOT NULL,
            rol_usuario ENUM('ESTUDIANTE', 'DOCENTE', 'ENCARGADO') NOT NULL
        ) ENGINE=InnoDB;
        """,
        # 2. Tabla Solicitudes Médicas (HU-01)
        """
        CREATE TABLE IF NOT EXISTS solicitudes_medicas (
            id_solicitud_medica INT AUTO_INCREMENT PRIMARY KEY,
            id_estudiante INT NOT NULL,
            nivel_urgencia ENUM('BAJA', 'MEDIA', 'ALTA') NOT NULL DEFAULT 'MEDIA',
            estado_solicitud ENUM('PENDIENTE', 'APROBADO', 'RECHAZADO', 'OBSERVADO') NOT NULL DEFAULT 'PENDIENTE',
            justificacion_dictamen TEXT NULL,
            id_operador INT NULL,
            fecha_ingreso DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_dictamen DATETIME NULL,
            FOREIGN KEY (id_estudiante) REFERENCES usuarios(id_usuario),
            FOREIGN KEY (id_operador) REFERENCES usuarios(id_usuario)
        ) ENGINE=InnoDB;
        """,
        # 3. Tabla Notificaciones (HU-01)
        """
        CREATE TABLE IF NOT EXISTS notificaciones (
            id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
            id_solicitud_medica INT NOT NULL,
            mensaje_notificacion TEXT NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_solicitud_medica) REFERENCES solicitudes_medicas(id_solicitud_medica) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """,
        # 4. Tabla Medicamentos (HU-02)
        """
        CREATE TABLE IF NOT EXISTS medicamentos (
            id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
            nombre_medicamento VARCHAR(100) NOT NULL,
            stock_medicamento INT NOT NULL DEFAULT 0
        ) ENGINE=InnoDB;
        """,
        # 5. Tabla Docentes Seguros (HU-03)
        """
        CREATE TABLE IF NOT EXISTS docentes_seguros (
            id_docente_seguro INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL UNIQUE,
            estado_seguro ENUM('HABILITADO', 'INHABILITADO') NOT NULL DEFAULT 'INHABILITADO',
            aportes_vigentes BOOLEAN DEFAULT FALSE,
            requisito_pendiente TEXT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """,
    ]

    @classmethod
    def crear_tablas(cls):
        """Crea todas las tablas requeridas si no existen."""
        conexion = ConexionBaseDatos.obtener_conexion()
        cursor = conexion.cursor()

        try:
            for sql_tabla in cls.TABLAS:
                cursor.execute(sql_tabla)
            conexion.commit()
            print("Tablas verificadas/creadas correctamente.")
        except Error as e:
            conexion.rollback()
            print(f"Error al crear las tablas: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def cargar_datos_iniciales(cls):
        """Inserta los datos iniciales de prueba si las tablas están vacías."""
        conexion = ConexionBaseDatos.obtener_conexion()
        cursor = conexion.cursor()

        try:
            # Insertar usuarios de prueba si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            if cursor.fetchone()[0] == 0:
                sql_usuarios = """
                INSERT INTO usuarios (nombre_usuario, rol_usuario) VALUES 
                ('Juan Perez', 'ESTUDIANTE'),
                ('Pedro Gomez', 'DOCENTE'),
                ('Carlos Mendoza', 'ENCARGADO')
                """
                cursor.execute(sql_usuarios)
                print("Datos iniciales de 'usuarios' cargados.")

            # Insertar medicamentos de prueba si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM medicamentos")
            if cursor.fetchone()[0] == 0:
                sql_medicamentos = """
                INSERT INTO medicamentos (nombre_medicamento, stock_medicamento) VALUES
                ('Paracetamol 500mg', 120),
                ('Ibuprofeno 400mg', 0),
                ('Amoxicilina 500mg', 30)
                """
                cursor.execute(sql_medicamentos)
                print("Datos iniciales de 'medicamentos' cargados.")

            conexion.commit()
        except Error as e:
            conexion.rollback()
            print(f"Error al cargar datos iniciales: {e}")
            raise e
        finally:
            cursor.close()

    @classmethod
    def inicializar_bd(cls):
        """Ejecuta el proceso completo de inicialización."""
        print("Iniciando la creación de la base de datos...")
        cls.crear_tablas()
        cls.cargar_datos_iniciales()
        print("Base de datos inicializada con éxito.")


if __name__ == "__main__":
    try:
        CreacionBaseDatos.inicializar_bd()
    finally:
        ConexionBaseDatos.cerrar_conexion()