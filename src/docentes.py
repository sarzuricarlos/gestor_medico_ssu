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

    @staticmethod
    def listar_docentes():
        """Devuelve la lista de todos los docentes con su id y nombre.
        Retorna una lista de tuplas (id_usuario, nombre_usuario).
        """
        sql = """
            SELECT usuarios.id_usuario, usuarios.nombre_usuario
            FROM usuarios
            INNER JOIN docentes_seguros ON docentes_seguros.id_usuario = usuarios.id_usuario
            WHERE usuarios.rol_usuario = 'DOCENTE'
            ORDER BY usuarios.nombre_usuario
        """
        filas = ConexionBaseDatos.ejecutar_consulta(sql)
        return [(f["id_usuario"], f["nombre_usuario"]) for f in filas]