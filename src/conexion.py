import sys
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# Asegurar que Python reconozca la raíz para importar config.py
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import config


class ConexionBaseDatos:
    _conexion = None

    @classmethod
    def obtener_conexion(cls):
        """Devuelve la conexión activa o crea una nueva utilizando la configuración con SSL."""
        if cls._conexion is None or not cls._conexion.is_connected():
            try:
                # Se desempaca el diccionario DB_CONFIG definido en config.py
                cls._conexion = mysql.connector.connect(**config.DB_CONFIG)
                print("Conexión exitosa a la base de datos (SSL habilitado).")
            except Error as e:
                print(f"Error al intentar conectar con la base de datos: {e}")
                raise e

        return cls._conexion

    @classmethod
    def cerrar_conexion(cls):
        """Cierra la conexión activa si está abierta."""
        if cls._conexion and cls._conexion.is_connected():
            cls._conexion.close()
            cls._conexion = None
            print("Conexión a la base de datos cerrada.")