# CRUD con Flask (desde 0 patatero)
Aquí tenemos un proyecto completo en el que vamos a programar un gestor de BBDD completo, el cual nos permitirá controlar la misma (Create, Read, Update, Delete), todo ello utilizando [Flask](https://flask.palletsprojects.com/en/stable/), [SQLAlchemy](https://www.sqlalchemy.org/), [SQLite](https://sqlite.org/) y [Bootstrap](https://getbootstrap.com/).

## Funcionalidades principales del proyecto
- Listado de productos
- Búsqueda de producto por nombre
- Ver los detalles de un producto
- Crear, editar o eliminar un producto
- Validar los formularios (forma básica)
- Informar al usuario mediante mensajes (flash)
- Se trabaja sobre una base de datos en SQLite3
- Se crea una estructura modular con Application Factory y Blueprint:
    - Blueprint: objetos que permiten definir las rutas, plantillas, recursos estáticos (PDF, imágenes...) y los modelos de forma modular, agurpados por funcionalidad específica.
    - Application Factory: patrón de diseño típico que instancia un objeto de aplicación, inicializa las extensiones y registra los Blueprints necesarios en cada funcionalidad, de forma que se configuran múltiples instancias de la aplicación a partir de un código base.
- Se realiza testing con la biblioteca pytest

## Estructura del proyecto
```text
crud_flask/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   ├── js/
│   │   └── pdf/
│   ├── templates/
│   │   ├── base.html
│   │   └── productos/
│   │       ├── _form.html
│   │       ├── create.html
│   │       ├── detail.html
│   │       └── index.html
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── routes.py
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── config.py
```

- `app/` -> carpeta que contiene todo el proyecto en Flask
    - `static/` -> carpeta que contiene archivos estáticos (sólo se entregan al navegador como CSS, imágenes, PDFs a servir, iconos, fuentes...)
    - `templates/` -> carpeta que guarda los archivos HTML de nuestra aplicación. Una template es un archivo HTML que puede recibir datos desde Python
        - `base.html` -> template principal que sirve para no repetir código en el resto de páginas
        - `productos/` -> carpetas que contiene templates de productos
            - `_form.html` -> formulario de producto
            - `create.html` -> editar un nuevo producto
            - `detail.html` -> muestra el detalle de un producto determinado
            - `index.html` -> página principal del CRUD de productos, muestra todos los productos de nuestra BBDD
    - `__init__.py` -> archivo que convierte la carpeta app en un paquete, organizando el proyecto y configurándolo. Este es el patrón APPLICATION FACTORY
    - `extensions.py` -> archivos que tiene las extensiones de Flask (SQLAlchemy)
    - `models.py` -> archivo que define los modelos de la BBDD. Un modelo representa a una tabla
    - `routes.py` -> archivo que contiene todas las rutas de Flask, o lo que es lo mismo, las URLs de la aplicaicón
- `.gitignore` -> se modela de forma que se escribe aquello que Git no debe "ver"
- `README.md` -> archivo para documentar el proyecto, orientado a GitHub
requirements.txt -> archivo que contienen las dependencias (librerías necesarias) del proyecto
- `run.py` -> archivo que arranque la aplicación Flask, al cual lo podemos "llamar" de 2 formas diferentes:
    - `python run.py`
    - `flask --app run.py --debug run`
- `config.py` -> archivo de configuración de la aplicación donde podemos encontrar la clave secreta de Flask, la ruta de la BBDD y la configuración de SQLAlchemy