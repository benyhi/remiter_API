from .database import ma
from marshmallow import validates, ValidationError
from .models import Remito, Cliente

class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    cuit = ma.auto_field()
    telefono = ma.auto_field()

    @validates('cuit')
    def validate_cuit(self, value):
        if not value.isdigit() or len(value) != 11:
            raise ValidationError('El CUIL debe contener solo números y tener 11 caracteres')

class RemitoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Remito

    id = ma.auto_field()
    numero = ma.auto_field()
    cliente_id = ma.Integer(required=True, load_only=True)
    cliente = ma.Nested(ClienteSchema, dump_only=True)
    fecha = ma.auto_field()
    productos = ma.auto_field()
    total = ma.auto_field()
