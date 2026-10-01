import mysql.connector
from mysql.connector import Error

import config


class ConexionBaseDatos:
    _conexion = None

    @classmethod
    def obtener_conexion(cls):
        """Devuelve la conexión activa o crea una nueva con SSL habilitado."""
        if cls._conexion is None or not cls._conexion.is_connected():
            try:
                cls._conexion = mysql.connector.connect(**config.DB_CONFIG)
                print("Conexión exitosa a la base de datos (SSL habilitado).")
            except Error as e:
                print(f"Error al conectar con la base de datos: {e}")
                raise e
        return cls._conexion

    @classmethod
    def cerrar_conexion(cls):
        if cls._conexion and cls._conexion.is_connected():
            cls._conexion.close()
            cls._conexion = None
            print("Conexión a la base de datos cerrada.")

    @classmethod
    def ejecutar_consulta(cls, sql, parametros=None):
        conexion = cls.obtener_conexion()
        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, parametros or ())
            return cursor.fetchall()
        except Error as e:
            print(f"Error en SELECT: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def ejecutar_transaccion(cls, sql, parametros=None):
        conexion = cls.obtener_conexion()
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, parametros or ())
            conexion.commit()
            return cursor.rowcount > 0
        except Error as e:
            conexion.rollback()
            print(f"Error en transacción: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()