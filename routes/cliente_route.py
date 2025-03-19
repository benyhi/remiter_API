from flask import Blueprint, request, jsonify
from controllers import ClienteController as Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

#CLIENTES

@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.get_all()
    return jsonify(clientes)

@cliente_bp.route('/clientes', methods=['POST'])
def post_cliente():
    data = request.get_json()
    cliente = Cliente.create(data)
    return jsonify(cliente)

@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.get_one(id)
    return jsonify(cliente)

@cliente_bp.route('/clientes', methods=['PUT'])   
def put_cliente():
    data = request.get_json()
    cliente = Cliente.update(data)
    return jsonify(cliente)

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.delete(id)
    return jsonify(cliente)

@cliente_bp.route('/clientes/import', methods=['POST'])
def import_clientes():
    data = request.get_json()
    path = data.get('path')
    clientes = Cliente.import_data(path)
    return jsonify(clientes)