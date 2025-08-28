from .database import db
from sqlalchemy import cast, Date

class Remito(db.Model):
    __tablename__ = 'remito'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete="CASCADE", name='fk_remito_cliente'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, server_default=cast(db.func.now(), Date))
    productos = db.Column(db.JSON, nullable=False)  # Almacenar productos como JSON
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
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuit = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)

class Factura(db.Model):
    __tablename__ = 'factura'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id', ondelete="CASCADE", name='fk_factura_proveedor'), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha = db.Column(db.Date, nullable=False, server_default=cast(db.func.now(), Date))
    monto = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Enum('pendiente','pago_parcial','pagado','cancelado','excedido', name='estado_enum'), nullable=False, default='pendiente')

    proveedor = db.relationship('Proveedor', backref=db.backref('facturas', cascade="all, delete"))    

    pagos = db.relationship(
        'Pago', 
        back_populates='factura', 
        cascade="all, delete-orphan",
        lazy="joined"
    )

    @property
    def total_pagado(self):
        return sum(p.monto_pagado for p in self.pagos)

    @property
    def saldo(self):
        return self.monto - self.total_pagado

    def actualizar_estado(self):
        """Actualiza el estado de la factura según los pagos."""
        if self.total_pagado == 0:
            self.estado = 'pendiente'
        elif self.total_pagado < self.monto:
            self.estado = 'pago_parcial'
        elif self.total_pagado == self.monto:
            self.estado = 'pagado'
        else:
            self.estado = 'excedido'

class Pago(db.Model):
    __tablename__ = 'pago'
    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id', ondelete="CASCADE", name='fk_pago_factura'), nullable=False)
    monto_pagado = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.Enum('efectivo','transferencia','cheque','deposito', name='metodo_pago_enum'), nullable=False, default='cheque')
    fecha = db.Column(db.Date, nullable=False, server_default=cast(db.func.now(), Date))

    factura = db.relationship(
        "Factura",
        back_populates="pagos"
    )

