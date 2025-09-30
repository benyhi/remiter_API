from .database import ma
from marshmallow import validates, ValidationError
from .models import Remito, Cliente, Proveedor, Factura, Pago, Documento, NotaCredito, CtaCte
from datetime import date

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
    fecha = ma.auto_field()
    productos = ma.auto_field()
    total = ma.auto_field()

    cliente = ma.Nested(ClienteSchema, dump_only=True)
    
class ProveedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proveedor
        load_instance = True

    documentos = ma.Nested("DocumentoSchema", many=True)
    cta_cte = ma.Nested("CtaCteSchema", many=True)
        
class ProveedorNomSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    id = ma.auto_field()
    nombre = ma.auto_field()
    
class DocumentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Documento
        load_instance = True
        include_fk = True

    proveedor = ma.Nested(ProveedorSchema)
    factura = ma.Nested("FacturaSchema")
    pago = ma.Nested("PagoSchema")
    nota_credito = ma.Nested("NotaCreditoSchema")
    cta_cte = ma.Nested("CtaCteSchema", many=True)

class FacturaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        load_instance = True
        include_fk = True

    documento = ma.Nested(DocumentoSchema)
    
class PagoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pago
        load_instance = True
        include_fk = True

    documento = ma.Nested(DocumentoSchema)

class NotaCreditoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotaCredito
        load_instance = True
        include_fk = True

    documento = ma.Nested(DocumentoSchema)

class CtaCteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CtaCte
        load_instance = True
        include_fk = True

    proveedor = ma.Nested(ProveedorSchema)
    documento = ma.Nested(DocumentoSchema)
