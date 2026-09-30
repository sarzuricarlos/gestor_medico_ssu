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
