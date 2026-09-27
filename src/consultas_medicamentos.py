from src.conexion import ConexionBaseDatos


class ConsultasMedicamentos:
    """Contiene las consultas relacionadas con los medicamentos."""

    @staticmethod
    def listar_medicamentos():
        """Obtiene todos los medicamentos registrados en la base de datos."""
        sql = (
            "SELECT "
            "medicamentos.id_medicamento, "
            "medicamentos.nombre_medicamento, "
            "medicamentos.stock_medicamento "
            "FROM medicamentos"
        )

        return ConexionBaseDatos.ejecutar_consulta(sql)

    @staticmethod
    def buscar_medicamentos(texto):
        """Busca medicamentos por nombre sin distinguir mayúsculas de minúsculas."""
        sql = (
            "SELECT "
            "medicamentos.id_medicamento, "
            "medicamentos.nombre_medicamento, "
            "medicamentos.descripcion_medicamento, "
            "medicamentos.stock_medicamento, "
            "medicamentos.disponible_medicamento "
            "FROM medicamentos "
            "WHERE LOWER(medicamentos.nombre_medicamento) LIKE LOWER(%s)"
        )
        parametros = (f"%{texto.strip()}%",)

        return ConexionBaseDatos.ejecutar_consulta(sql, parametros)
