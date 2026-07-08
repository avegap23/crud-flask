# archivo routes.py --> las rutas de la app web, es decir, las URLs
'''
def mi_decorador(funcion):
    def envoltorio():
        print("antes de ejecutar la función, aparece esta línea")
        funcion()
        print("despueś de ejecutar la función, aparece esta otra línea)

        return envoltorio
-------------------------------------------------
@mi_decorador
def saludar()
    print("hola")    
-------------------------------------------------
saludar()

RESULTADO EN CONSOLA:
1ª línea: antes de ejecutar la función, aparece esta línea
2ª línea: hola
3ª línea: después de ejecutar la función, aparece esta otra línea

---------------------------------------------------------------------------------------------------

SQLAlchemy es un ORM, el cual trata a la BBDD como si fuese una clase:
    · tabla = clase
    · cada fila = instancia de clase
    · cada columna = atributos de clase
    · FK = relaciones entre clases

Tabla cliente: id, nombre y apellidos
class Cliente:
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)

VENTAJAS:
    - accedes a tablas y filas de una BBDD como si fuese una clase u objeto
    - casi siempre, no te hace falta "tocar" SQL, el ORM se encarga de todo
    - es independiente de la BBDD, es decir, podemos cambiar "cosas" sin problema ni más código extra
    - más productividad
'''

# IMPORTS -----------------------------------------------------------------------------------------
from decimal import Decimal, InvalidOperation # https://docs.python.org/3/library/decimal.html
from flask import Blueprint, flash, redirect, render_template, request, url_for

from .extensions import db # importación de todo lo relativo a la BBDD
from .models import Product # importación de la clase "modelo" para la creación de productos

# BLUEPRINTS --------------------------------------------------------------------------------------
# Blueprint: controlamos que las templates estén en la carpeta PRODUCTS
products_bp = Blueprint("products", __name__)

# FUNCTIONS ---------------------------------------------------------------------------------------
# Validación de formularios y sus respectivos campos
def validate_product_form(form): # se envía el formulario completo, chequeamos todo "a una"
    """Validación de los datos enviados desde el formulario de Flask-HTML"""
    errores = [] # creación de array de errores, donde se van a guardar los errores encontrados

    # recibimos los datos
    name = form.get("name", "").strip() # recibe el campo o cadena vacía si no existe, quitando los espacios de antes y después
    description = form.get("description", "").strip()
    price_raw = form.get("price", "").strip().replace(",",".") # reemplazamos la , por un .
    stock_raw = form.get("stock", "").strip()

    # comprobación (ahora sí)
    # a.- validación del nombre
    if not name:
        errores.append("¡El nombre es obligatorio!")
    
    # b.- validación del precio
    try:
        price = Decimal(price_raw) # casting para convertir a número decimal
        if price < 0:
            errores.append("¡El precio no puede ser negativo!")
    except (InvalidOperation, ValueError): # contemplamos errores de valor y de operaciones inválidas
        price = Decimal("0.00")
        errores.append("El precio debe tener un formato de número válido")

    # c.- validación del stock
    try:
        stock = int(stock_raw) # casting para convertir a entero
        if stock < 0:
            errores.append("¡El stock no puede ser negativo!")
    except ValueError: # contemplamos errores de valor y de operaciones inválidas
        stock = 0
        errores.append("El stock debe ser un número entero")
    
    # d.- retornamos todos los errores que se hayan producido y los datos "en limpio"
    return errores, {"name":name, "description":description, "price":price, "stock":stock}

# Creación de rutas en Flask y redirecciones al usuario
# a.- home: cuando se visite /, se activa la función home
@products_bp.route("/") # @ decorador, modifica el comportamiento de una función
def home():
    return redirect(url_for("products.index"))

# b.- lista de productos: permite admés la búsqueda por nombre
@products_bp.route("/products") # la url sería .../products
def index():
    # 1.- obtener la petición de la URL por parte del usuario
    q = request.args.get("q","").strip() # obtención del parámetro de la URL
    # /products?q=teclado --> el usuario entró buscando teclados

    # 2.- pedir a la BBDD el listado de productos (completo) o la query
    statement = db.select(Product).order_by(Product.created_at.desc())
    # pedimos los productos y los ordenamos en modo descendente de creación

    if q:
        statement = statement.where(Product.name.ilike(f"%{q}%"))
        # añadimos un filtro donde la query estará contenida en un texto, da igual lo que haya antes y después
        # ilike no hace casesensitive
    
    # 3.- Ejecutamos la correspondiente consulta
    productos = db.session.execute(statement).scalars().all()
    # db.session.execute(statement): ejecuta la consulta
    # scalars(): extrae los objetos Product, en vez de una fila completa
    # all(): convierte el resultado en una lista [Product(name="teclado"), Product(name="ratón")]

    # 4.- renderizamos la plantilla
    return render_template("productos/index.html", products=productos, q=q)

# c.- detalle del producto
@products_bp.route("/products/<int:product_id>") # la URL sería .../products/<ID>
def detail(product_id):
    producto = db.get_or_404(Product, product_id) # me da el producto o un 404 si no existe
    return render_template("productos/detail.html", product=producto)

# d.- creación de nuevos productos
@products_bp.route("/products/new", methods=["GET", "POST"]) # la url sería .../products/new
# GET muestra página/formulario -- POST procesa los datos enviados
def create():
    # 1.- comprobar si el formulario ha sido enviado
    if request.method == "POST":
        errores, datos = validate_product_form(request.form)
        # errores encontrados, datos limpios
    
        # 1.1.- Si no hay errores, se muestran los datos de la BBDD
        if not errores:
            product = Product(**datos) # **datos --> desempaqueta el diccionario con los datos limpios
            db.session.add(product) # añade el product a la sesión, antes de su guardado en BBDD
            db.session.commit() # guardamos el producto "de verdad" en la BBDD

            flash("El producto se ha creado correctamente", "success") # creamos una alerta al usuario
            return redirect(url_for("products.detail", product_id=product.id))
            # product_id=product.id compara que la ID sea la misma en la BBDD, pasa la ID del producto
        
        # 1.2.- Hay errores, mostramos información al usuario
        for error in errores:
            flash(error, "danger")
        
        return render_template("productos/create.html", product=datos), 400
        # se vuelve a mostrar el formulario de creación de producto
        # product=datos: el formulario conserva los datos que escribe el usuario
        # 400: significa BAD REQUEST, el formulario llegó, pero los datos no son válidos
    
    return render_template("productos/create.html", product=None)
    # se ejecuta cuando el usuario entra por 1ª vez a la página "crear", mostrando un formulario totalmente vacío

# e.- editar un producto
@products_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
# GET muestra página/formulario -- POST procesa los datos enviados
def edit(product_id):
    # 0.- comprobar si existe el producto o 404 si no está en la BBDD
    product = db.get_or_404(Product, product_id)
    
    # 1.- comprobar si el formulario ha sido enviado
    if request.method == "POST":
        errores, datos = validate_product_form(request.form)
        # errores encontrados, datos limpios
    
        # 1.1.- Si no hay errores, se muestran los datos de la BBDD
        if not errores:
            product.name = datos["name"]
            product.description = datos["description"]
            product.price = datos["price"]
            product.stock = datos["stock"]
            db.session.commit()

            flash("El producto se ha actualizado correctamente", "success")
            return redirect(url_for("products.detail", product_id=product.id))
        
        # 1.2.- Hay errores, mostramos información al usuario
        for error in errores:
            flash(error, "danger")
        
        return render_template("productos/edit.html", product=datos), 400
        # product=datos: el formulario conserva los datos que escribe el usuario
        # 400: significa BAD REQUEST, el formulario llegó, pero los datos no son válidos
    
    return render_template("productos/edit.html", product=None)

# f.- borrar un producto
@products_bp.route("/products/<int:product_id>/delete", methods=["POST"])
def delete(product_id):
    # 0.- comprobar si existe el producto o 404 si no está en la BBDD
    product = db.get_or_404(Product, product_id)

    # 1.- se realizan las demás operaciones
    db.session.delete(product) # borra el producto a la sesión, antes de su guardado en BBDD
    db.session.commit() # borramos el producto "de verdad" en la BBDD

    flash("El producto se borró correctamente", "success") # creamos una alerta al usuario
    return redirect(url_for("products.index"))