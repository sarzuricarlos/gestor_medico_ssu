class SesionUsuario:
    """Mantiene en memoria los datos del usuario que inició sesión."""

    _id_usuario = None
    _nombre_usuario = None
    _id_rol = None

    @classmethod
    def iniciar_sesion(cls, id_usuario, nombre_usuario, id_rol):
        """Guarda los datos del usuario autenticado."""
        cls._id_usuario = id_usuario
        cls._nombre_usuario = nombre_usuario
        cls._id_rol = id_rol

    @classmethod
    def cerrar_sesion(cls):
        """Elimina los datos del usuario de la memoria."""
        cls._id_usuario = None
        cls._nombre_usuario = None
        cls._id_rol = None

    @classmethod
    def hay_sesion_activa(cls):
        """Indica si existe un usuario con sesión iniciada."""
        return cls._id_usuario is not None

    @classmethod
    def obtener_id_usuario(cls):
        return cls._id_usuario

    @classmethod
    def obtener_nombre_usuario(cls):
        return cls._nombre_usuario

    @classmethod
    def obtener_id_rol(cls):
        return cls._id_rol
