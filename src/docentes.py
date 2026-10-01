from src.conexion import ConexionBaseDatos


class DocenteRepository:
    """Capa de datos para la afiliación de docentes (HU-03)."""

    @staticmethod
    def obtener_estado_seguro_docente(id_usuario):
        """Consulta el estado del seguro, aportes y requisitos pendientes de un docente."""
        sql = """
            SELECT
                docentes_seguros.estado_seguro,
                docentes_seguros.aportes_vigentes,
                docentes_seguros.requisito_pendiente
            FROM docentes_seguros
            INNER JOIN usuarios ON usuarios.id_usuario = docentes_seguros.id_usuario
            WHERE docentes_seguros.id_usuario = %s
        """
        resultado = ConexionBaseDatos.ejecutar_consulta(sql, (id_usuario,))
        return resultado[0] if resultado else None