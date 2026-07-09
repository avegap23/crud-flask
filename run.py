"""Punto de entrada de la aplicación"""

from __future__ import annotations # https://docs.python.org/3/library/__future__.html#future__.annotations
import os # https://docs.python.org/3/library/os.html

from app import create_app # procedente del archivo __init__.py

app = create_app() # creación de un objeto APP

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"), # localhost, accesible sólo desde mi propia máquina
        port=int(os.getenv("PORT", "5000")), # puerto de escucha para la APP
        debug=app.config.get("DEBUG", False) # control de modo debug, desactivado en producción
    )