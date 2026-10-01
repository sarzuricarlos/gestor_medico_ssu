import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carga variables desde un archivo .env si está presente
load_dotenv()


def obtener_ruta_recurso(ruta_relativa):
    """
    Obtiene la ruta absoluta a un recurso, funcionando tanto en desarrollo
    como dentro de un ejecutable generado con PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        # Estamos dentro de un .exe empaquetado por PyInstaller
        base = Path(sys._MEIPASS)
    else:
        # Estamos en desarrollo normal
        base = Path(__file__).resolve().parent
    return base / ruta_relativa


# Directorio raíz del proyecto y ruta al certificado SSL
BASE_DIR = Path(__file__).resolve().parent
CA_PEM_PATH = obtener_ruta_recurso("ca.pem")

# Constantes globales de conexión
DB_HOST = os.getenv("DB_HOST", "mysql-3b77147e-postres-bd.e.aivencloud.com")
DB_PORT = int(os.getenv("DB_PORT", 16646))
DB_USER = os.getenv("DB_USER", "avnadmin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "AVNS_gATB_5v408jk2NgoDwB")
DB_NAME = os.getenv("DB_NAME", "defaultdb")

# Ruta absoluta al certificado SSL/CA
DB_SSL_CA = str(CA_PEM_PATH) if CA_PEM_PATH.exists() else None
DB_SSL_VERIFY_CERT = os.getenv("DB_SSL_VERIFY_CERT", "True").lower() in ("true", "1", "yes")

# Diccionario unificado para MySQL / Aiven
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "ssl_ca": DB_SSL_CA,
    "ssl_verify_cert": DB_SSL_VERIFY_CERT,
}