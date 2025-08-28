from models.models import Factura, Proveedor, Pago
from models.schemas import FacturaSchema, FacturaDetalleSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

class FacturaController:

	@staticmethod
	def get_all():
		try:
			facturas = db.session.query(Factura).all()
			return FacturaSchema(many=True).dump(facturas)
		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudieron obtener las facturas: {str(e)}")

	@staticmethod
	def get_all_with_detail():
		try:
			facturas = (
				db.session.query(Factura)
				.options(joinedload(Factura.pagos))  # eager load
				.order_by(Factura.fecha.desc())
				.all()
			)
			return FacturaDetalleSchema(many=True).dump(facturas)

		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudieron obtener las facturas con detalle: {str(e)}")
		
	@staticmethod
	def get_one(factura_id):
		try:
			factura = db.session.get(Factura, factura_id)
			if not factura:
				return None
			return FacturaSchema().dump(factura)
		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudo obtener la factura: {str(e)}")
		
	@staticmethod
	def get_all_by_id(proveedor_id):
		try:
			facturas = db.session.query(Factura
				).filter(Factura.proveedor_id == proveedor_id
			 	).order_by(Factura.fecha.desc()).all()
			if not facturas:
				return None
			return FacturaSchema(many=True).dump(facturas)
		except SQLAlchemyError as e:
			raise Exception(f"No se pudo obtener las facturas del proveedor id: {str(e)}")
		
	@staticmethod
	def get_all_by_id_with_detail(proveedor_id):
		try:
			facturas = (
				db.session.query(Factura)
				.options(joinedload(Factura.pagos)) 
				.filter(Factura.proveedor_id == proveedor_id)
				.order_by(Factura.fecha.desc())
				.all()
			)
			return FacturaDetalleSchema(many=True).dump(facturas)

		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudieron obtener las facturas del proveedor: {str(e)}")

	@staticmethod
	def create(data):
		try:
			proveedor_id = data.get("proveedor_id")
			numero = data.get("numero")
			descripcion = data.get("descripcion")
			fecha = data.get("fecha")
			monto = data.get("monto")
			estado = data.get("estado", "pendiente")

			if not proveedor_id or not numero or monto is None:
				raise Exception("Datos incompletos para crear la factura")

			proveedor = db.session.get(Proveedor, proveedor_id)
			if not proveedor:
				raise Exception("Proveedor no encontrado")

			factura = Factura(
				proveedor_id=proveedor_id,
				numero=numero,
				descripcion=descripcion,
				fecha=fecha,
				monto=monto,
				estado=estado
			)
			db.session.add(factura)
			db.session.commit()
			return FacturaSchema().dump(factura)
		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudo crear la factura: {str(e)}")

	@staticmethod
	def update(data):
		try:
			factura_id = data.get("id")
			factura = db.session.get(Factura, factura_id)
			if not factura:
				return None

			for key in ["numero", "descripcion", "fecha", "monto", "estado", "proveedor_id"]:
				if key in data:
					setattr(factura, key, data[key])

			db.session.commit()
			return FacturaSchema().dump(factura)
		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudo actualizar la factura: {str(e)}")

	@staticmethod
	def delete(factura_id):
		try:
			factura = db.session.get(Factura, factura_id)
			if not factura:
				return None
			db.session.delete(factura)
			db.session.commit()
			return FacturaSchema().dump(factura)
		except SQLAlchemyError as e:
			db.session.rollback()
			raise Exception(f"No se pudo eliminar la factura: {str(e)}")
