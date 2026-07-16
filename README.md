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
│   │       ├── edit.html
│   │       └── index.html
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── routes.py
├── instance/
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
            - `_form.html` -> template de formulario de producto
            - `create.html` -> template de creación de producto
            - `detail.html` -> template de detalle de un producto determinado
            - `edit.html` -> template de edición de producto
            - `index.html` -> template de la página principal del CRUD de productos; muestra todos los productos de nuestra BBDD
    - `__init__.py` -> archivo que convierte la carpeta app en un paquete, organizando el proyecto y configurándolo. Este es el patrón APPLICATION FACTORY
    - `extensions.py` -> archivos que tiene las extensiones de Flask (SQLAlchemy)
    - `models.py` -> archivo que define los modelos de la BBDD. Un modelo representa a una tabla
    - `routes.py` -> archivo que contiene todas las rutas de Flask, o lo que es lo mismo, las URLs de la aplicación
- `instance/` -> carpeta que se creará al iniciarse una instancia de la aplicación, la cual utilizará para trabajar y almacenar cosas
- `.gitignore` -> se modela de forma que se escribe aquello que Git no debe "ver"
- `README.md` -> archivo para documentar el proyecto, orientado a GitHub
requirements.txt -> archivo que contienen las dependencias (librerías necesarias) del proyecto
- `run.py` -> archivo que arranque la aplicación Flask, al cual lo podemos "llamar" de 2 formas diferentes:
    - `python run.py`
    - `flask --app run.py --debug run`
- `config.py` -> archivo de configuración de la aplicación donde podemos encontrar la clave secreta de Flask, la ruta de la BBDD y la configuración de SQLAlchemy

## Instalación
### 1. Requisitos

- Git
- Python 3.10 o superior recomendado
- pip

### 2.1. Instalación en Linux/MacOS

```bash
git clone https://github.com/avegap23/crud-flask.git
cd crud-flask
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2.2. Instalación en Windows PowerShell

```powershell
git clone https://github.com/avegap23/crud-flask.git
cd crud-flask
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Crear la base de datos

```bash
flask --app run.py init-db
```

### 4. Insertar datos de ejemplo, opcional

```bash
python seed.py
```

## Ejecutar el servidor

```
cp .env.example .env
flask --app run.py --debug run
```

Luego abre:
```text
http://127.0.0.1:5000/login
```

Credenciales por defecto de la APP:
```text
usuario: admin
contraseña: admin123
```

## Configuración mínima para producción
```bash
export APP_ENV=production
export SECRET_KEY="clave-larga-aleatoria"
export SESSION_COOKIE_SECURE=true
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD_HASH="hash-generado-por-Werkzeug"
```

Luego abre:

```text
http://127.0.0.1:5000/
```

## Ejecutar tests

```bash
pytest
```

## Rutas principales

| Método | Ruta | Acción |
|---|---|---|
| GET | `/products` | Listar productos |
| GET | `/products?q=texto` | Buscar productos |
| GET | `/products/new` | Formulario de creación |
| POST | `/products/new` | Crear producto |
| GET | `/products/<id>` | Ver detalle |
| GET | `/products/<id>/edit` | Formulario de edición |
| POST | `/products/<id>/edit` | Actualizar producto |
| POST | `/products/<id>/delete` | Eliminar producto |

## Nota de seguridad

Este proyecto es ideal para aprender la base de un CRUD. Para producción conviene añadir autenticación, CSRF, migraciones con Flask-Migrate, variables de entorno para `SECRET_KEY`, logs, paginación y control de permisos.

## Endurecimiento sobre nuestro CRUD
En base al despliegue v1.0, se desarrolla una capa básica de seguridad sobre el CRUD.

### Cambios principales en la v2.0

1. **Secretos por variables de entorno**
    - Secret Key sin fijar
    - En producción, la app no va a arrancar si no tenemos disponible la Secret Key.

2. **Debug desactivado por defecto**
    - La app no ejecuta el modo debug de forma fija
    - Se posibilita activar el debug utilizando FLASK_DEBUG

3. **Autenticación simple**
    - Se protege todo el CRUD por sesión
    - Para desarrollo se va a utilizar un usuario diferente al de producción
    - En producción necesitaremos que las contraseñas lleven hash

4. **Protección CSRF**
    - Todos los formularios POST incorporan un token
    - Las peticiones sin token devuelven un error [404 (Bad Request)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)

5. **Cabeceras HTTP de seguridad**
    - Activación de Content-Security-Policy
    - Activación de X-Frame-Options:DENY
    - Activación de X-Content-Type-Options: nosniff
    - Activación de Referrer-Policy
    - Activación de Permissions-Policy

6. **Cookies de sesión securizadas**
    - Activación de HttpOnly, SameSite=Lx y SEcure para HTTPS

7. **Validaciones más reforzadas**
    - Control sobre la longitud de nombre y descripción
    - Control sobre precios (no negativo, finito, con 2 decimales)
    - Control de stock (no negativo y con límite máximo)
    - Escape de comodines en las búsquedas (en SQL, utilizando lso LIKEs)

8. **Restricciones de la BBDD**
    - Control para evitar precios/stock negativos a nivel de BBDD (en SQL, utilizando los CHECK)

9. **Limpieza de los entregables**
    - Las carpetas pycache, instance, así como los archivos .en no se deben versionar
    - La BBDD SQLite3 local no se incluye en un zip entregable "endurecido"

## Más documentación en:

<h4><a href="https://avegap23.github.io/crud-flask-docs/" target="_blank">https://avegap23.github.io/crud-flask-docs/</a></h4>
