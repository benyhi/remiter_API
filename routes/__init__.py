from .remito_route import remitos_bp
from .cliente_route import cliente_bp
from .proveedor_route import proveedor_bp
from .documento_route import documentos_bp
from .cta_cte_route import cta_cte_bp

def register_blueprint(app):
    app.register_blueprint(remitos_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(documentos_bp)
    app.register_blueprint(cta_cte_bp)
    

    