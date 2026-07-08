# Archivo principal de la aplicación

from app import create_app # procedente del archivo __init__.py

app = create_app() # creación de un objeto APP

if __name__ == "__main__":
    app.run(debug=True)