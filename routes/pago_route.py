from flask import Blueprint, request, jsonify
from controllers.pago_controller import PagoController as Pago

pago_bp = Blueprint('pago_bp', __name__)

@pago_bp.route('/pagos', methods=['GET'])
def get_pagos():
    try:
        pagos = Pago.get_all()
        return jsonify(pagos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pago_bp.route('/pagos', methods=['POST'])
def post_pago():
    data = request.get_json()
    try:
        nuevo_pago = Pago.create(data)
        return jsonify(nuevo_pago), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pago_bp.route('/pagos/<int:id>', methods=['GET'])
def get_pago(id):
    try:
        pago = Pago.get_one(id)
        if pago is None:
            return jsonify({"error": "Pago no encontrado"}), 404
        return jsonify(pago), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pago_bp.route('/pagos', methods=['PUT'])
def put_pago():
    data = request.get_json()
    try:
        pago_actualizado = Pago.update(data)
        if pago_actualizado is None:
            return jsonify({"error": "Pago no encontrado"}), 404
        return jsonify(pago_actualizado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pago_bp.route('/pagos/<int:id>', methods=['DELETE'])
def delete_pago(id):
    try:
        pago_eliminado = Pago.delete(id)
        if pago_eliminado is None:
            return jsonify({"error": "Pago no encontrado"}), 404
        return jsonify(pago_eliminado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
