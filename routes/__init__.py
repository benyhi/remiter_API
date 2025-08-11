from .remito_route import remitos_bp
from .cliente_route import cliente_bp
from .proveedor_route import proveedor_bp
from .factura_route import factura_bp
from .pago_route import pago_bp

def register_blueprint(app):
    app.register_blueprint(remitos_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(factura_bp)
    app.register_blueprint(pago_bp)

    