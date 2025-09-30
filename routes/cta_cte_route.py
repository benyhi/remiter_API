from flask import Blueprint, request, jsonify
from controllers.cta_cte_controller import CtaCteController

cta_cte_bp = Blueprint("cta_cte", __name__, url_prefix="/cta_cte")

# Listar todos los registros de CtaCte
@cta_cte_bp.route("/", methods=["GET"])
def get_all_cta_cte():
    try:
        return jsonify(CtaCteController.get_all())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Listar todos con detalle (proveedor y documento)
@cta_cte_bp.route("/detalle", methods=["GET"])
def get_all_cta_cte_with_detail():
    try:
        return jsonify(CtaCteController.get_all_with_detail())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Obtener un registro por ID
@cta_cte_bp.route("/<int:cta_id>", methods=["GET"])
def get_cta_cte(cta_id):
    try:
        registro = CtaCteController.get_one(cta_id)
        if not registro:
            return jsonify({"error": "Registro no encontrado"}), 404
        return jsonify(registro)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Listar registros por proveedor
@cta_cte_bp.route("/proveedor/<int:proveedor_id>", methods=["GET"])
def get_cta_cte_by_proveedor(proveedor_id):
    try:
        registros = CtaCteController.get_all_by_proveedor(proveedor_id)
        if not registros:
            return jsonify([])
        return jsonify(registros)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Crear un registro de CtaCte
@cta_cte_bp.route("/", methods=["POST"])
def create_cta_cte():
    try:
        data = request.json
        registro = CtaCteController.create(data)
        return jsonify(registro), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Actualizar un registro de CtaCte
@cta_cte_bp.route("/", methods=["PUT"])
def update_cta_cte():
    try:
        data = request.json
        registro = CtaCteController.update(data)
        if not registro:
            return jsonify({"error": "Registro no encontrado"}), 404
        return jsonify(registro)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un registro de CtaCte
@cta_cte_bp.route("/<int:cta_id>", methods=["DELETE"])
def delete_cta_cte(cta_id):
    try:
        registro = CtaCteController.delete(cta_id)
        if not registro:
            return jsonify({"error": "Registro no encontrado"}), 404
        return jsonify(registro)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
