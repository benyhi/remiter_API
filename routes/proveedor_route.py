from flask import Blueprint, request, jsonify
from controllers.documento_controller import DocumentosController
from controllers.proveedor_controller import ProveedorController as Proveedor

proveedor_bp = Blueprint('proveedor_bp', __name__)

@proveedor_bp.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        proveedores = Proveedor.get_all()
        return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@proveedor_bp.route('/proveedores', methods=['POST'])
def post_proveedor():
    data = request.get_json()
    try:
        nuevo_proveedor = Proveedor.create(data)
        return jsonify(nuevo_proveedor), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@proveedor_bp.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = Proveedor.get_one(id)
        if proveedor is None:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        return jsonify(proveedor), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Obtener todos los documentos de un proveedor (anidados)
@proveedor_bp.route('/<int:proveedor_id>/documentos', methods=['GET'])
def get_documentos_by_proveedor(proveedor_id):
    try:
        documentos = DocumentosController.get_all_by_proveedor(proveedor_id)
        if not documentos:
            return jsonify([]), 200
        return jsonify(documentos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener todos los documentos de un proveedor con detalle (relaciones)
@proveedor_bp.route('/<int:proveedor_id>/documentos/detalle', methods=['GET'])
def get_documentos_detalle_by_proveedor(proveedor_id):
    try:
        # Este método carga relaciones: factura, pago, nota_credito, cta_cte
        documentos = DocumentosController.get_all_with_detail()
        # Filtramos por proveedor
        documentos = [d for d in documentos if d['proveedor_id'] == proveedor_id]
        if not documentos:
            return jsonify([]), 200
        return jsonify(documentos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@proveedor_bp.route('/proveedores', methods=['PUT'])
def put_proveedor():
    data = request.get_json()
    try:
        proveedor_actualizado = Proveedor.update(data)
        if proveedor_actualizado is None:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        return jsonify(proveedor_actualizado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        proveedor_eliminado = Proveedor.delete(id)
        if proveedor_eliminado is None:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        return jsonify(proveedor_eliminado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
