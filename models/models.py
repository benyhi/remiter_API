from .database import db
from sqlalchemy import cast, Date
from sqlalchemy import func
from sqlalchemy.orm import object_session
from decimal import Decimal

class Remito(db.Model):
    __tablename__ = 'remito'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete="CASCADE", name='fk_remito_cliente'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, server_default=cast(db.func.now(), Date))
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
    estado = db.Column(db.Enum('pendiente','pago_parcial','pagado','cancelado', name='estado_enum'), nullable=False, default='pendiente')

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

   
    def actualizar_estado(self, session=None):
        """
        Recalcula el total de pagos y fija el estado de la factura:
          - total_pagado == 0                 -> 'pendiente'
          - 0 < total_pagado < monto          -> 'pago_parcial'
          - total_pagado == monto             -> 'pagado'
        Usa sum() a nivel DB para mayor robustez.
        """
        from .models import Pago
        sess = session or object_session(self) or db.session

        if not self.id:
            return

        total_pagado = (
            sess.query(func.coalesce(func.sum(Pago.monto_pagado), 0.0))
            .filter(Pago.factura_id == self.id)
            .scalar()
        ) or 0.0

        monto = self.monto or 0.0

        total_dec = Decimal(str(total_pagado))
        monto_dec = Decimal(str(monto))

        if total_dec == Decimal('0'):
            nuevo_estado = 'pendiente'
        elif total_dec < monto_dec:
            nuevo_estado = 'pago_parcial'
        else:
            nuevo_estado = 'pagado'

        # Solo escribir si cambió (reduce writes innecesarias)
        if getattr(self, 'estado', None) != nuevo_estado:
            self.estado = nuevo_estado
            # marcar la factura para persistir (si se pasa session se añadirá en el event/controller)
            try:
                sess.add(self)
            except Exception:
                pass

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

