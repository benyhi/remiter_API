from flask import Blueprint, request, jsonify
from controllers.factura_controller import FacturaController as Factura

factura_bp = Blueprint('factura_bp', __name__)

@factura_bp.route('/facturas', methods=['GET'])
def get_facturas():
	try:
		facturas = Factura.get_all()
		return jsonify(facturas), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500
	
@factura_bp.route('/facturas/detalle', methods=['GET'])
def get_facturas_with_detail():
	try:
		facturas = Factura.get_all_with_detail()
		return jsonify(facturas), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@factura_bp.route('/facturas', methods=['POST'])
def post_factura():
	data = request.get_json()
	try:
		nueva_factura = Factura.create(data)
		return jsonify(nueva_factura), 201
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@factura_bp.route('/facturas/<int:id>', methods=['GET'])
def get_factura(id):
	try:
		factura = Factura.get_one(id)
		if factura is None:
			return jsonify({"error": "Factura no encontrada"}), 404
		return jsonify(factura), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@factura_bp.route('/facturas', methods=['PUT'])
def put_factura():
	data = request.get_json()
	try:
		factura_actualizada = Factura.update(data)
		if factura_actualizada is None:
			return jsonify({"error": "Factura no encontrada"}), 404
		return jsonify(factura_actualizada), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@factura_bp.route('/facturas/<int:id>', methods=['DELETE'])
def delete_factura(id):
	try:
		factura_eliminada = Factura.delete(id)
		if factura_eliminada is None:
			return jsonify({"error": "Factura no encontrada"}), 404
		return jsonify(factura_eliminada), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500
