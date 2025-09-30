from models.models import CtaCte, Proveedor, Documento
from models.schemas import CtaCteSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

class CtaCteController:

    @staticmethod
    def get_all():
        try:
            registros = db.session.query(CtaCte).all()
            return CtaCteSchema(many=True).dump(registros)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los registros de CtaCte: {str(e)}")

    @staticmethod
    def get_all_with_detail():
        try:
            registros = (
                db.session.query(CtaCte)
                .options(
                    joinedload(CtaCte.proveedor),
                    joinedload(CtaCte.documento)
                )
                .order_by(CtaCte.fecha.desc())
                .all()
            )
            return CtaCteSchema(many=True).dump(registros)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los registros de CtaCte con detalle: {str(e)}")

    @staticmethod
    def get_one(cta_id):
        try:
            registro = db.session.get(CtaCte, cta_id)
            if not registro:
                return None
            return CtaCteSchema().dump(registro)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo obtener el registro de CtaCte: {str(e)}")

    @staticmethod
    def get_all_by_proveedor(proveedor_id):
        try:
            registros = (
                db.session.query(CtaCte)
                .filter(CtaCte.proveedor_id == proveedor_id)
                .order_by(CtaCte.fecha.desc())
                .all()
            )
            if not registros:
                return None
            return CtaCteSchema(many=True).dump(registros)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los registros de CtaCte del proveedor: {str(e)}")

    @staticmethod
    def create(data):
        try:
            proveedor_id = data.get("proveedor_id")
            documento_id = data.get("documento_id")
            fecha = data.get("fecha")
            descripcion = data.get("descripcion")
            debe = data.get("debe", 0)
            haber = data.get("haber", 0)
            saldo = data.get("saldo", 0)

            if not proveedor_id:
                raise Exception("Proveedor es obligatorio para crear el registro de CtaCte")

            proveedor = db.session.get(Proveedor, proveedor_id)
            if not proveedor:
                raise Exception("Proveedor no encontrado")

            registro = CtaCte(
                proveedor_id=proveedor_id,
                documento_id=documento_id,
                fecha=fecha,
                descripcion=descripcion,
                debe=debe,
                haber=haber,
                saldo=saldo
            )

            db.session.add(registro)
            db.session.commit()
            return CtaCteSchema().dump(registro)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo crear el registro de CtaCte: {str(e)}")

    @staticmethod
    def update(data):
        try:
            cta_id = data.get("id")
            registro = db.session.get(CtaCte, cta_id)
            if not registro:
                return None

            for key in ["proveedor_id", "documento_id", "fecha", "descripcion", "debe", "haber", "saldo"]:
                if key in data:
                    setattr(registro, key, data[key])

            db.session.commit()
            return CtaCteSchema().dump(registro)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo actualizar el registro de CtaCte: {str(e)}")

    @staticmethod
    def delete(cta_id):
        try:
            registro = db.session.get(CtaCte, cta_id)
            if not registro:
                return None
            db.session.delete(registro)
            db.session.commit()
            return CtaCteSchema().dump(registro)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo eliminar el registro de CtaCte: {str(e)}")
