# archivo config.py
# contiene la configuración base de la app en Flask

"""Configuración centralizada de la app Flask.
La configuración sensible (producción) se optiene mediante las variables de entorno.
En desarrollo, se permiten valores por defecto para facilitar el aprendizaje, si bien
en producción la aplicación falla si falta la SECRET_KEY o la contraseña de administrador."""

# IMPORTS -----------------------------------------------------------------------------------------
from __future__ import annotations # https://docs.python.org/3/library/__future__.html#future__.annotations
import os # https://docs.python.org/3/library/os.html
import secrets # https://docs.python.org/3/library/secrets.html
from datetime import timedelta # https://docs.python.org/3/library/datetime.html
from pathlib import Path # https://docs.python.org/3/library/pathlib.html

# VARIABLES ---------------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent # obtenermos la ruta absoluta (/) del proyecto

# _env_bool son de uso interno, es decir, "tocan" parámetros muy importantes para el entorno
def _env_bool(name:str, default:bool = False) -> bool:
    """Convierte las variables de entorno tipo True/False a booleanos"""
    value = os.getenv(name)

    if value is None:
        return default # si no hay variable, el entorno se crea por defecto
    
    return value.strip().lower() in {"1", "True", "yes", "on", "si", "si"}

# CLASSES -----------------------------------------------------------------------------------------
# Clase Config: contiene la configuaración de Flask
class Config:
    """Configuración base segura para desarrollo y despliegue de la aplicación"""

    # 1.- Configuración de la APP sin modificar el código fuente
    APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
    DEBUG = _env_bool("FLASK_DEBUG", False) # modo DEBUG desactivado
    TESTING = _env_bool("TESTING", False) # modo testeo desactivado

    # 2.- Configuración de clave secreta y de la firma de tokens (CSRF)
    SECRET_KEY = os.getenv("SECRET_KEY") # busca la SECRET_KEY. Si no está, la crea con valor None

    if APP_ENV == "producción" and not SECRET_KEY:
        raise RuntimeError("¡Debes definir la SECRET_KEY en producción!")
    
    # si se nos olvida crear la SECRET_KEY
    if not SECRET_KEY:
        SECRET_KEY = "dev-" + secrets.token_urlsafe(32)
        # la clave será: dev-texto_aleatorio_seguro_usando_32_bytes(43 caracteres compatibles con URLs)

    # 3.- BBDD: configuramos la ruta donde se encuentra la BBDD - comunicaicón con la BBDD
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'bbdd.sqlite'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # para evitar que SQLAlchemy rastree objetos

    # 4.- Control de cookies de sesión
    SESSION_COOKIE_NAME = "crud_session" # nombre de la cookie en el navegador
    SESSION_COOKIE_HTTONLY = True # el navegador envía la cookie al servidor sin JS
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", APP_ENV == "production")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.getenv("SESSION_LIFETIME_MINUTES", "60")))
    SESSION_REFRESH_EACH_REQUEST = False # evitamos renovar las cookies de sesión en cada petición 

    #5.- Control de limitación de tamaño de petición: evitamos envíos gigantes al formulario
    MAX_CONTENT_LENGTH = int (os.getenv("MAX_CONTENT_LENGTH", str(1*1024*1024)))
    # 1*1024*1024 = 1.048.576 bytes -> 1 MB

    # 6.- Cabeceras & CSRF: activando las protecciones de seguridad globales del CRUD
    SECURITY_HEADERS_ENABLED = _env_bool("SECURITY_HEADERS_ENABLED", True)
    # activación de cabeceras HTTP seguras (protección contra ciberataques)
    CSRF_ENABLED = _env_bool("CSRF_ENABLED", True)
    # evita el Cross-Site Request Forgery, ataque externo que intenta obligar a que el navegador envíe acciones a la APP sin permiso

    # 7.- Control de autenticación simple (protección básica del CRUD)
    REQUIRE_LOGIN = _env_bool("REQUIRE_LOGIN", True) # requerimos logeo para trabajar con el CRUD
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH") # blindaje de la contraseña mediante cifrados básicos
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # Si estoy en producción, estoy logueado y no tengo hash
    if APP_ENV == "production" and REQUIRE_LOGIN and not ADMIN_PASSWORD_HASH:
        raise RuntimeError("¡Debes definir ADMIN_PASSWORD_HASH para producción!")
    
    # si no tengo ADMIN_PASSWORD y estamos en develop
    if not ADMIN_PASSWORD and APP_ENV != "production":
        ADMIN_PASSWORD = "admin123" # solo para desarrollo, hay que cambiarlo en producción