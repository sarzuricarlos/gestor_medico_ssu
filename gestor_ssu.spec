# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Recolectar archivos de customtkinter (temas, JSONs internos)
datos_customtkinter = collect_data_files("customtkinter")

# Recolectar submodulos ocultos que PyInstaller no detecta
hidden_imports = collect_submodules("customtkinter")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("ca.pem", "."),          # Incluir el certificado SSL en la raíz del .exe
        ("config.py", "."),       # Por si acaso
    ] + datos_customtkinter,
    hiddenimports=hidden_imports + [
        # MySQL
        "mysql.connector",
        "mysql.connector.plugins",
        "mysql.connector.plugins.caching_sha2_password",
        "mysql.connector.plugins.mysql_native_password",
        "mysql.connector.plugins.sha256_password",
        # dotenv
        "dotenv",
        # ✅ Tus módulos internos
        "src",
        "src.conexion",
        "src.solicitudes",
        "src.medicamentos",
        "src.docentes",
        "src.sesion",
        "src.notificaciones",
        "src.creacionbd",
        "src.app_seguro",
        "src.vistas",
        "src.vistas.ventana_dictamen",
        "src.vistas.frame_consulta_medicamentos",
        "src.vistas.frame_estado_seguro_docente",
        "src.vistas.frame_gestion_solicitudes",
        "src.vistas.tarjeta_medicamento",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="GestorMedicoSSU",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)