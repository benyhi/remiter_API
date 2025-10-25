from .database import ma
from marshmallow import validates, ValidationError, fields
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
        include_relationships = False

    documentos = ma.Nested("DocumentoSchema", many=True, dump_only=True)
    cta_cte = ma.Nested("CtaCteSchema", many=True, dump_only=True)
        
class ProveedorNomSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proveedor

    id = ma.auto_field()
    nombre = ma.auto_field()
    cuit = ma.auto_field()
    telefono = ma.auto_field()
    email = ma.auto_field()
    direccion = ma.auto_field()
    
class DocumentoSchemaLight(ma.SQLAlchemyAutoSchema):
    """Schema ligero para documentos sin relaciones anidadas."""
    class Meta:
        model = Documento
        load_instance = True
        include_fk = True

    fecha = fields.String()
    proveedor = ma.Nested(ProveedorNomSchema, dump_only=True)

class DocumentoSchema(ma.SQLAlchemyAutoSchema):
    """"Schema completo para documentos con relaciones anidadas."""
    class Meta:
        model = Documento
        load_instance = True
        include_fk = True

    fecha = fields.String()
    proveedor = ma.Nested(ProveedorNomSchema, dump_only=True)
    factura = ma.Nested("FacturaSchema", dump_only=True)
    pago = ma.Nested("PagoSchema", dump_only=True)
    nota_credito = ma.Nested("NotaCreditoSchema", dump_only=True)
    cta_cte = ma.Nested("CtaCteSchema", many=True, dump_only=True)

class FacturaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        load_instance = True
        include_fk = True

    documento = ma.Nested(DocumentoSchemaLight, dump_only=True)
    
class PagoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pago
        load_instance = True
        include_fk = True

    documento = ma.Nested(DocumentoSchemaLight, dump_only=True)

class NotaCreditoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotaCredito
        load_instance = True
        include_fk = True

    documento = ma.Nested(DocumentoSchemaLight, dump_only=True)

class CtaCteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CtaCte
        load_instance = True
        include_fk = True

    fecha = fields.Date()
    proveedor = ma.Nested(ProveedorNomSchema, dump_only=True)
    documento = ma.Nested(DocumentoSchemaLight, dump_only=True)
