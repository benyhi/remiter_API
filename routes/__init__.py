from .remito_route import remitos_bp
from .cliente_route import cliente_bp

def register_blueprint(app):
    app.register_blueprint(remitos_bp)
    app.register_blueprint(cliente_bp)

    