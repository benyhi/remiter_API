from .database import db
from datetime import date
from sqlalchemy import cast, Date

class Remito(db.Model):
    __tablename__ = 'remito'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete="CASCADE", name='fk_remito_cliente'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    productos = db.Column(db.JSON, nullable=False)
    total = db.Column(db.Float, nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('remitos', cascade="all, delete"))

    @classmethod
    def get_remito_number(cls):
        last_remito = db.session.query(cls).order_by(cls.numero.desc()).first()
        return (last_remito.numero +1) if last_remito else 1

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuit = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=True)

class Proveedor(db.Model):
    __tablename__ = "proveedor"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuit = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(150))

    documentos = db.relationship("Documento", back_populates="proveedor")
    cta_cte = db.relationship("CtaCte", back_populates="proveedor")


class Documento(db.Model):
    __tablename__ = "documentos"
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedor.id"), nullable=False)
    tipo = db.Column(db.String(20))  # factura, pago, nc
    fecha = db.Column(db.Date, default=date.today, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(255))

    proveedor = db.relationship("Proveedor", back_populates="documentos")
    factura = db.relationship("Factura", uselist=False, back_populates="documento")
    pago = db.relationship("Pago", uselist=False, back_populates="documento")
    nota_credito = db.relationship("NotaCredito", uselist=False, back_populates="documento")
    cta_cte = db.relationship("CtaCte", back_populates="documento")


class Factura(db.Model):
    __tablename__ = "factura"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey("documentos.id"), unique=True)

    documento = db.relationship("Documento", back_populates="factura")


class Pago(db.Model):
    __tablename__ = "pago"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey("documentos.id"), unique=True)
    metodo_pago = db.Column(db.String(50))

    documento = db.relationship("Documento", back_populates="pago")


class NotaCredito(db.Model):
    __tablename__ = "nota_credito"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey("documentos.id"), unique=True)

    documento = db.relationship("Documento", back_populates="nota_credito")


class CtaCte(db.Model):
    __tablename__ = "cta_cte"
    id = db.Column(db.Integer, primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedor.id"), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey("documentos.id"))
    fecha = db.Column(db.Date, server_default=cast(db.func.now(), Date))
    descripcion = db.Column(db.String(255))
    debe = db.Column(db.Float, default=0)
    haber = db.Column(db.Float, default=0)
    saldo = db.Column(db.Float, default=0)

    proveedor = db.relationship("Proveedor", back_populates="cta_cte")
    documento = db.relationship("Documento", back_populates="cta_cte")