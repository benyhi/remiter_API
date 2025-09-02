from models.models import Pago, Factura
from models.schemas import PagoSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError

class PagoController:

    @staticmethod
    def get_all():
        try:
            pagos = Pago.query.order_by(Pago.fecha.desc()).all()
            return PagoSchema(many=True).dump(pagos)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los pagos: {str(e)}")

    @staticmethod
    def get_one(pago_id):
        try:
            pago = db.session.get(Pago, pago_id)
            if not pago:
                return None
            return PagoSchema().dump(pago)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo obtener el pago: {str(e)}")
        
    @staticmethod
    def create(data):
        try:
            factura_id = data.get("factura_id")
            monto_pagado = data.get("monto_pagado")
            metodo_pago = data.get("metodo_pago", "cheque")
            fecha = data.get("fecha")

            if not factura_id or monto_pagado is None:
                raise Exception("Datos incompletos para crear el pago")

            factura = db.session.get(Factura, factura_id)
            if not factura:
                raise Exception("Factura no encontrada")

            pago = Pago(
                factura_id=factura_id,
                monto_pagado=monto_pagado,
                metodo_pago=metodo_pago,
                fecha=fecha
            )
            db.session.add(pago)

            # No establecemos estado manualmente: el listener lo recalculará
            db.session.commit()
            return PagoSchema().dump(pago)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo crear el pago: {str(e)}")

    @staticmethod
    def update(data):
        try:
            pago_id = data.get("id")
            pago = db.session.get(Pago, pago_id)
            if not pago:
                return None

            for key in ["factura_id", "monto_pagado", "metodo_pago", "fecha"]:
                if key in data:
                    setattr(pago, key, data[key])

            # No setear estado manualmente; listener (after_flush_postexec) lo recalculará.
            db.session.commit()
            return PagoSchema().dump(pago)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo actualizar el pago: {str(e)}")

    @staticmethod
    def delete(pago_id):
        try:
            pago = db.session.get(Pago, pago_id)
            if not pago:
                return None
            payload = PagoSchema().dump(pago)
            db.session.delete(pago)
            # listener detectará la eliminación y ajustará la factura asociada
            db.session.commit()
            return payload
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo eliminar el pago: {str(e)}")
