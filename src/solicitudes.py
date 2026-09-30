from mysql.connector import Error
from src.conexion import ConexionBaseDatos

ESTADOS_DICTAMEN = ("APROBADO", "RECHAZADO", "OBSERVADO")

ORDENES = {
    "urgencia": "nivel_urgencia DESC, fecha_ingreso DESC",
    "antiguas": "fecha_ingreso ASC",
    "recientes": "fecha_ingreso DESC",
}


def actualizar_dictamen_solicitud(id_solicitud, estado, justificacion, id_operador):
    """Registra el dictamen de una solicitud médica con fecha_dictamen = NOW().
    Devuelve True si se actualizó la solicitud, False si el id no existe.
    """
    if estado not in ESTADOS_DICTAMEN:
        raise ValueError(f"Estado inválido: {estado}. Use uno de {ESTADOS_DICTAMEN}")

    sql = """
        UPDATE solicitudes_medicas
        SET estado_solicitud = %s,
            justificacion_dictamen = %s,
            id_operador = %s,
            fecha_dictamen = NOW()
        WHERE id_solicitud_medica = %s
    """
    conexion = ConexionBaseDatos.obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(sql, (estado, justificacion, id_operador, id_solicitud))
        conexion.commit()
        return cursor.rowcount > 0
    except Error as e:
        conexion.rollback()
        print(f"Error al actualizar el dictamen: {e}")
        raise
    finally:
        cursor.close()


class SolicitudRepository:
    """Capa de datos para las solicitudes médicas."""

    @staticmethod
    def listar_solicitudes(orden="recientes"):
        """Lista todas las solicitudes ordenadas según el criterio indicado."""
        if orden not in ORDENES:
            raise ValueError(f"Orden inválido: {orden}. Use uno de {tuple(ORDENES)}")

        sql = f"""
            SELECT id_solicitud_medica, id_estudiante, nivel_urgencia,
                   estado_solicitud, fecha_ingreso
            FROM solicitudes_medicas
            ORDER BY {ORDENES[orden]}
        """
        return ConexionBaseDatos.ejecutar_consulta(sql)

    @staticmethod
    def obtener_solicitudes_pendientes(orden="recientes"):
        """Obtiene solo las solicitudes en estado PENDIENTE, ordenadas."""
        if orden not in ORDENES:
            raise ValueError(f"Orden inválido: {orden}. Use uno de {tuple(ORDENES)}")

        sql = f"""
            SELECT id_solicitud_medica, id_estudiante, nivel_urgencia,
                   estado_solicitud, fecha_ingreso
            FROM solicitudes_medicas
            WHERE estado_solicitud = 'PENDIENTE'
            ORDER BY {ORDENES[orden]}
        """
        return ConexionBaseDatos.ejecutar_consulta(sql)