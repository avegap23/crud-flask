# archivo __init__.py
# convierte app en un paquete

'''
__name__: dice a Flask donde está ubicada la aplicación
instance_relative_config=True: dice a Flask que utilice la carpeta especial instance:
    - guardamos "cosas locales":
        · la BBDD en SQLite
        · la configuración privada
        · archivos que no se van a commitear en Git
.mkdir: creación de carpeta
    · parents=True: si faltan carpetas intermedias, créalas también
    · exist_ok=True: si la carpeta existe, no me des error
'''

# IMPORTS -----------------------------------------------------------------------------------------
from pathlib import Path # https://docs.python.org/3/library/pathlib.html
from flask import Flask # https://flask.palletsprojects.com/en/stable/
from config import Config # importación del archivo de configuración
from .extensions import db # importación de db desde el archivo extensions.py

# FUNCTIONS ---------------------------------------------------------------------------------------
# Creación de la app, recibe el archivo config.py
def create_app(config_class=Config):
    # 1.- Creación de la app como tal
    app = Flask(__name__, instance_relative_config=True)

    # 2.- Cargo la configuración de la app
    app.config.from_object(config_class)

    # 3.- Creación de la carpeta instance si no existe
    Path(app.instance_path).mkdir(parents=True,exist_ok=True)

    # 4.- Conexión BBDD: SQLAlchemy se conecta con Flask
    db.init_app(app)

    # 5.- Importación de Blueprints (que agrupan rutas)
    from .routes import products_bp # evitamos importaciones circulares

    # 6.- Inyecta un coomando en la terminal
    @app.cli.command("init-db")
    def init_db_command():
        """Creación de las tablas de la base de datos"""
        db.create_all()
        print("BBDD inicializada correctamente")
        
    return app # retornamos la app creada y configurada