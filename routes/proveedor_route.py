from flask import Blueprint, request, jsonify
from controllers.documento_controller import DocumentosController
from controllers.proveedor_controller import ProveedorController as Proveedor
from models.schemas import (
    DocumentoSchemaLight,
    DocumentoSchema,
    ProveedorNomSchema,
    ProveedorSchema,
)

proveedor_bp = Blueprint('proveedor_bp', __name__)

# --- LISTA DE PROVEEDORES (liviano) ---
@proveedor_bp.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        proveedores = Proveedor.get_all()
        data = ProveedorNomSchema(many=True).dump(proveedores)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- CREAR NUEVO PROVEEDOR ---
@proveedor_bp.route('/proveedores', methods=['POST'])
def post_proveedor():
    try:
        data = request.get_json()
        proveedor = Proveedor.create(data)
        data = ProveedorSchema().dump(proveedor)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- OBTENER DETALLE COMPLETO DE UN PROVEEDOR ---
@proveedor_bp.route('/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = Proveedor.get_one(id)
        if not proveedor:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        data = ProveedorSchema().dump(proveedor)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ACTUALIZAR UN PROVEEDOR ---
@proveedor_bp.route('/proveedores/<int:id>', methods=['PUT'])
def put_proveedor(id):
    try:
        data = request.get_json()
        proveedor_actualizado = Proveedor.update(id, data)
        if not proveedor_actualizado:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        data = ProveedorSchema().dump(proveedor_actualizado)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ELIMINAR PROVEEDOR ---
@proveedor_bp.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        result = Proveedor.delete(id)
        if not result:
            return jsonify({"error": "Proveedor no encontrado"}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- DOCUMENTOS DE UN PROVEEDOR (liviano) ---
@proveedor_bp.route('/proveedores/<int:proveedor_id>/documentos', methods=['GET'])
def get_documentos_by_proveedor(proveedor_id):
    try:
        documentos = DocumentosController.get_all_by_proveedor(proveedor_id)
        data = DocumentoSchema(many=True).dump(documentos)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- DOCUMENTOS CON DETALLE COMPLETO ---
@proveedor_bp.route('/proveedores/<int:proveedor_id>/documentos/detalle', methods=['GET'])
def get_documentos_detalle_by_proveedor(proveedor_id):
    try:
        documentos = DocumentosController.get_all_with_detail(proveedor_id)
        data = DocumentoSchema(many=True).dump(documentos)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
