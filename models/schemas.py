from .database import ma
from marshmallow import validates, ValidationError
from .models import Remito, Cliente, Proveedor, Factura, Pago

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
            raise ValidationError('El CUIT debe contener solo números y tener 11 caracteres')

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

class ProveedorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    cuit = ma.auto_field()
    telefono = ma.auto_field()
    email = ma.auto_field()
    direccion = ma.auto_field()

    @validates('cuit')
    def validate_cuit(self, value):
        if not value.isdigit() or len(value) != 11:
            raise ValidationError('El CUIT debe contener solo números y tener 11 caracteres')
        
    @validates('email')
    def validate_email(self, value):
        if value and '@' not in value:
            raise ValidationError('El email debe ser válido')
        
class ProveedorNomSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    id = ma.auto_field()
    nombre = ma.auto_field()
    
class PagoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pago
    
    id = ma.auto_field()
    factura_id = ma.Integer(required=True, load_only=True)
    monto_pagado = ma.auto_field()
    metodo_pago = ma.auto_field()
    fecha = ma.auto_field()

    @validates('monto_pagado')
    def validate_monto_pagado(self, value):
        if value <= 0:
            raise ValidationError('El monto pagado debe ser mayor a cero')
        
class FacturaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Factura
    
    id = ma.auto_field()
    numero = ma.auto_field()
    proveedor = ma.Nested(ProveedorNomSchema, dump_only=True)
    descripcion = ma.auto_field()
    fecha = ma.auto_field()
    monto = ma.auto_field()
    estado = ma.auto_field()
    pagos = ma.Nested(PagoSchema, many=True, dump_only=True)

    @validates('monto')
    def validate_monto(self, value):
        if value <= 0:
            raise ValidationError('El monto debe ser mayor a cero')
