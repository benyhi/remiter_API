from flask import Blueprint, request, jsonify
from controllers import ClienteController as Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = Cliente.get_all()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def post_cliente():
    data = request.get_json()
    try:
        nuevo_cliente = Cliente.create(data)
        return jsonify(nuevo_cliente), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    try:
        cliente = Cliente.get_one(id)
        if cliente is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(cliente), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes', methods=['PUT'])   
def put_cliente():
    data = request.get_json()
    try:
        cliente_actualizado = Cliente.update(data)
        if cliente_actualizado is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(cliente_actualizado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        cliente_eliminado = Cliente.delete(id)
        if cliente_eliminado is None:
            return jsonify({"error": "Cliente no encontrado"}), 404
        return jsonify(cliente_eliminado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes/import', methods=['POST'])
def import_clientes():
    data = request.get_json()
    path = data.get('path')
    try:
        clientes_importados = Cliente.import_data(path)
        return jsonify(clientes_importados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
