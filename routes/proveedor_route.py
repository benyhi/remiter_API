from flask import Blueprint, request, jsonify
from controllers.proveedor_controller import ProveedorController as Proveedor
from controllers.factura_controller import FacturaController as Factura

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
    
@proveedor_bp.route('/proveedores/<int:id>/facturas', methods=['GET'])
def get_facturas_by_proveedor(id):
    try:
        facturas = Factura.get_all_by_id(id)
        return jsonify(facturas), 200
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
