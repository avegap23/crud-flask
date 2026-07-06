# archivo models.py
# modelado de, en este caso, los productos
'''
NOTAS:
class Product(db.Model): no es una clase cualquiera... hereda de db.Model, de modo
que SQLAlchemy entiende que esta nueva clase será una tabla de la BBDD
'''

# IMPORT ------------------------------------------------------------------------------------------
from datetime import datetime, timezone # https://docs.python.org/3/library/datetime.html
from decimal import Decimal # https://docs.python.org/3/library/decimal.html

from .extensions import db # importación del objeto de tipo BBDD, para trabajar con SQLAlchemy

# CLASS -------------------------------------------------------------------------------------------
class Product(db.Model):
    # 1.- Nombre de la tabla en la BBDD --> ATRIBUTO DE CLASE
    __tablename__ = "products" # se puede quitar, ya que SQLAlchemy lo puede hacer automáticamente

    # 2.- "montamos el festival" de la BBDD --> MÉTODO CONSTRUCTOR
    id = db.Column(db.Integer, primary_key=True) # PK
    name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10,2), nullable=False, default=Decimal("0.00")) # (10,2) 10 dígitos, 2 decimales
    stock = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) # si no pasamos fecha, se crea automáticamente la fecha actual UTC
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc), # fecha actual (creación)
        onupdate=lambda: datetime.now(timezone.utc) # cuando el producto se actualice, cambia la hora por la de ese momento
    )

    # 3.- Aplicamos el molde --> MÉTODOS DE LA CLASE
    def __repr__(self) -> str: # devuelve un string
        # __repr__ intenta mostrar algo que se entienda
        return f"producto {self.id} - {self.name!r}" # devuelve un texto
        # !r hace que el string aparezca con las comillas: "teclado"