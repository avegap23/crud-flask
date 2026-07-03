# Archivo principal de la aplicación

from flask import Flask # https://flask.palletsprojects.com/en/stable/

app = Flask(__name__)

@app.route("/") # definimos la URL principal de la app
def inicio():
    return "Hola, tienes Flask en funcionamiento"

if __name__ == "__main__":
    app.run(debug=True)