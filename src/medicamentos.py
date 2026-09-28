from src.conexion import ConexionBaseDatos


class MedicamentoRepository:
    def buscar_medicamentos_por_nombre(self, nombre):
        """Busca medicamentos cuyo nombre contenga el texto, sin distinguir mayúsculas."""
        conexion = ConexionBaseDatos.obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id_medicamento, nombre_medicamento, stock_medicamento
                FROM medicamentos
                WHERE LOWER(nombre_medicamento) LIKE LOWER(%s)
                ORDER BY nombre_medicamento
                """,
                (f"%{nombre.strip()}%",),
            )
            filas = cursor.fetchall()
            conexion.commit()  # cierra la lectura para ver datos nuevos al recargar
            return filas
        finally:
            cursor.close()
