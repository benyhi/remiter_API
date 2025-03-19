from flask import Blueprint, request, jsonify, render_template
from controllers import RemitoController as Remito

remitos_bp = Blueprint('remitos_bp', __name__)

#REMITOS

@remitos_bp.route('/remitos', methods=['GET'])
def get_remitos():
    remitos = Remito.get_all()
    return jsonify(remitos)

@remitos_bp.route('/remitos', methods=['POST'])
def post_remito():
    data = request.get_json()
    remito = Remito.create(data)
    return jsonify(remito)

@remitos_bp.route('/remitos/<int:id>', methods=['GET'])
def get_remito(id):
    remito = Remito.get_one(id)
    return jsonify(remito)

@remitos_bp.route('/remitos', methods=['PUT'])
def put_remito():
    data = request.get_json()
    remito = Remito.update(data)
    return jsonify(remito)

@remitos_bp.route('/remitos/<int:id>', methods=['DELETE'])
def delete_remito(id):
    remito = Remito.delete(id)
    return jsonify(remito)

@remitos_bp.route('/remitos/pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    response = Remito.generate_pdf(data)
    return response