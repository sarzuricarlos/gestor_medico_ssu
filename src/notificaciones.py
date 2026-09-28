from src.conexion import ConexionBaseDatos


class Notificaciones:
    """Contiene las consultas relacionadas con las notificaciones."""

    @staticmethod
    def crear_notificacion_estudiante(id_usuario, id_solicitud, mensaje):
        """Registra el aviso automatico de una solicitud medica para su estudiante."""
        # Inserta solo si la solicitud pertenece al estudiante indicado
        sql = (
            "INSERT INTO notificaciones (id_solicitud_medica, mensaje_notificacion) "
            "SELECT solicitudes_medicas.id_solicitud_medica, %s "
            "FROM solicitudes_medicas "
            "WHERE solicitudes_medicas.id_solicitud_medica = %s "
            "AND solicitudes_medicas.id_estudiante = %s"
        )

        return ConexionBaseDatos.ejecutar_transaccion(
            sql, (mensaje, id_solicitud, id_usuario)
        )
