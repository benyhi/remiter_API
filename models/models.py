from .database import db

class Remito(db.Model):
    __tablename__ = 'remito'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id', ondelete="CASCADE", name='fk_remito_cliente'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    productos = db.Column(db.JSON, nullable=False)  # Almacenar productos como JSON
    total = db.Column(db.Float, nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('remitos', cascade="all, delete"))

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'cliente_id': self.cliente_id,
            'fecha': self.fecha,
            'productos': self.productos,
            'total': self.total
        }

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

    def to_dict(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "cuit": self.cuit,
            "telefono": self.telefono
        }