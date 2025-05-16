from flask import Blueprint, request, jsonify
from controllers import RemitoController as Remito

remitos_bp = Blueprint('remitos_bp', __name__)

@remitos_bp.route('/remitos', methods=['GET'])
def get_remitos():
    try:
        remitos, status = Remito.get_all()
        return jsonify(remitos), status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@remitos_bp.route('/remitos', methods=['POST'])
def post_remito():
    try:
        data = request.get_json()
        remito, status = Remito.create(data)
        return jsonify(remito), status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@remitos_bp.route('/remitos/<int:id>', methods=['GET'])
def get_remito(id):
    try:
        remito, status = Remito.get_one(id)
        return jsonify(remito), status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@remitos_bp.route('/remitos/<int:id>', methods=['PUT'])
def put_remito(id):
    try:
        data = request.get_json()
        remito, status = Remito.update(id, data)
        return jsonify(remito), status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@remitos_bp.route('/remitos/<int:id>', methods=['DELETE'])
def delete_remito(id):
    try:
        remito, status = Remito.delete(id)
        return jsonify(remito), status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@remitos_bp.route('/remitos/pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        response, status = Remito.generate_pdf(data)
        return response, status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500

@remitos_bp.route('/remitos/pdf/<int:id>/print', methods=['POST'])
def print_pdf(id):
    try:
        response, status = Remito.print_pdf(id)
        return response, status
    except Exception as e:
        return jsonify({"error": "Error inesperado", "details": str(e)}), 500
