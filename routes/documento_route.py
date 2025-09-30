from flask import Blueprint, request, jsonify
from controllers.documento_controller import DocumentosController

documentos_bp = Blueprint("documentos", __name__, url_prefix="/documentos")

# Listar todos los documentos
@documentos_bp.route("/", methods=["GET"])
def get_all_documentos():
    try:
        return jsonify(DocumentosController.get_all())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Listar todos los documentos con detalle
@documentos_bp.route("/detalle", methods=["GET"])
def get_all_documentos_with_detail():
    try:
        return jsonify(DocumentosController.get_all_with_detail())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener un documento por ID
@documentos_bp.route("/<int:documento_id>", methods=["GET"])
def get_documento(documento_id):
    try:
        doc = DocumentosController.get_one(documento_id)
        if not doc:
            return jsonify({"error": "Documento no encontrado"}), 404
        return jsonify(doc)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Listar documentos por proveedor
@documentos_bp.route("/proveedor/<int:proveedor_id>", methods=["GET"])
def get_documentos_by_proveedor(proveedor_id):
    try:
        docs = DocumentosController.get_all_by_proveedor(proveedor_id)
        if not docs:
            return jsonify([])
        return jsonify(docs)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Crear un documento
@documentos_bp.route("/", methods=["POST"])
def create_documento():
    try:
        data = request.json
        doc = DocumentosController.create(data)
        return jsonify(doc), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Actualizar un documento
@documentos_bp.route("/", methods=["PUT"])
def update_documento():
    try:
        data = request.json
        doc = DocumentosController.update(data)
        if not doc:
            return jsonify({"error": "Documento no encontrado"}), 404
        return jsonify(doc)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un documento
@documentos_bp.route("/<int:documento_id>", methods=["DELETE"])
def delete_documento(documento_id):
    try:
        doc = DocumentosController.delete(documento_id)
        if not doc:
            return jsonify({"error": "Documento no encontrado"}), 404
        return jsonify(doc)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
