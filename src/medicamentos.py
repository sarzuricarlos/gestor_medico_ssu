from src.conexion import ConexionBaseDatos


class MedicamentoRepository:
    """Capa de datos para medicamentos (HU-02)."""

    @staticmethod
    def obtener_todos_medicamentos():
        """Lista todos los medicamentos registrados."""
        sql = (
            "SELECT id_medicamento, nombre_medicamento, stock_medicamento "
            "FROM medicamentos"
        )
        return ConexionBaseDatos.ejecutar_consulta(sql)

    @staticmethod
    def buscar_medicamentos_por_nombre(nombre):
        """Busca medicamentos por nombre usando LIKE insensible a mayúsculas."""
        sql = (
            "SELECT id_medicamento, nombre_medicamento, stock_medicamento "
            "FROM medicamentos "
            "WHERE LOWER(nombre_medicamento) LIKE LOWER(%s)"
        )
        return ConexionBaseDatos.ejecutar_consulta(sql, (f"%{nombre}%",))