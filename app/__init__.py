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

"""Application Factory: crea y conecta las piezas principales de Flask"""

# IMPORTS -----------------------------------------------------------------------------------------
from __future__ import annotations # https://docs.python.org/3/library/__future__.html#future__.annotations
from pathlib import Path # https://docs.python.org/3/library/pathlib.html
from flask import Flask, render_template
# https://flask.palletsprojects.com/en/stable/
# https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates

from config import Config # importación del archivo de configuración
from .extensions import db # importación de db desde el archivo extensions.py

# FUNCTIONS ---------------------------------------------------------------------------------------
# Creación de la app, recibe el archivo config.py
def create_app(config_class=Config):
    """Crea una instancia configurada de la aplicación Flask"""

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
    app.register_blueprint(products_bp) # registro para que funcionen las rutas

    # 6.- Inyecta un coomando en la terminal
    @app.cli.command("init-db")
    def init_db_command():
        """Creación de las tablas de la base de datos"""
        db.create_all()
        print("BBDD inicializada correctamente")

    # 7.- Contemplando y maquetando los posibles errores
    @app.errorhandler(400)
    def bad_request(error):
        return render_template("errors/error.html", code=400, title="Petición no válida", error=error), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/error.html", code=404, title="Página no encontrada", error=error), 404
    
    @app.errorhandler(413)
    def payload_too_large(error):
        return render_template("errors/error.html", code=413, title="Petición excesivamente grande", error=error), 413
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template("errors/error.html", code=500, title="Error interno", error=error), 500
        
    return app # retornamos la app creada y configurada