# archivo config.py
# contiene la configuración base de la app en Flask

# IMPORTS -----------------------------------------------------------------------------------------
from pathlib import Path # https://docs.python.org/3/library/pathlib.html

# VARIABLES ---------------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent # obtenermos la ruta absoluta (/) del proyecto

# CLASSES -----------------------------------------------------------------------------------------
# Clase Config: contiene la configuaración de Flask
class Config:
    SECRET_KEY = "a_cambiar_en_producción"

    # BBDD: configuramos la ruta donde se encuentra la BBDD - comunicaicón con la BBDD
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'bbdd.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False # para evitar que SQLAlchemy rastree objetos