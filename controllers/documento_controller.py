from models.models import Documento, Proveedor, Factura, Pago, NotaCredito
from models.schemas import DocumentoSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

class DocumentosController:

    @staticmethod
    def get_all():
        try:
            documentos = db.session.query(Documento).all()
            return DocumentoSchema(many=True).dump(documentos)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los documentos: {str(e)}")

    @staticmethod
    def get_all_with_detail():
        try:
            documentos = (
                db.session.query(Documento)
                .options(joinedload(Documento.factura),
                         joinedload(Documento.pago),
                         joinedload(Documento.nota_credito),
                         joinedload(Documento.cta_cte))
                .order_by(Documento.fecha.desc())
                .all()
            )
            return DocumentoSchema(many=True).dump(documentos)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los documentos con detalle: {str(e)}")

    @staticmethod
    def get_one(documento_id):
        try:
            documento = db.session.get(Documento, documento_id)
            if not documento:
                return None
            return DocumentoSchema().dump(documento)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo obtener el documento: {str(e)}")
        
    @staticmethod
    def get_all_by_proveedor(proveedor_id):
        try:
            documentos = (
                db.session.query(Documento)
                .filter(Documento.proveedor_id == proveedor_id)
                .order_by(Documento.fecha.desc())
                .all()
            )
            if not documentos:
                return None
            return documentos
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los documentos del proveedor: {str(e)}")

    @staticmethod
    def create(data):
        try:
            proveedor_id = data.get("proveedor_id")
            tipo = data.get("tipo")
            fecha = data.get("fecha")
            monto = data.get("monto")
            descripcion = data.get("descripcion")
            numero = data.get("numero")
            metodo_pago = data.get("metodo_pago")

            if not proveedor_id or not tipo or monto is None:
                raise Exception("Datos incompletos para crear el documento")

            proveedor = db.session.get(Proveedor, proveedor_id)
            if not proveedor:
                raise Exception("Proveedor no encontrado")

            documento = Documento(
                proveedor_id=proveedor_id,
                tipo=tipo,
                fecha=fecha,
                monto=monto,
                descripcion=descripcion
            )

            if tipo == "factura":
                documento.factura = Factura(numero=numero)
            elif tipo == "pago":
                documento.pago = Pago(numero=numero, metodo_pago=metodo_pago)
            elif tipo == "nota_credito":
                documento.nota_credito = NotaCredito(numero=numero)
            else:
                raise Exception(f"Tipo de documento no válido: {tipo}")

            db.session.add(documento)
            db.session.commit()

            return DocumentoSchema().dump(documento)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo crear el documento: {str(e)}")

    @staticmethod
    def update(data):
        try:
            documento_id = data.get("id")
            documento = db.session.get(Documento, documento_id)
            if not documento:
                return None

            for key in ["proveedor_id", "tipo", "fecha", "monto", "descripcion"]:
                if key in data:
                    setattr(documento, key, data[key])

            db.session.commit()
            return DocumentoSchema().dump(documento)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo actualizar el documento: {str(e)}")

    @staticmethod
    def delete(documento_id):
        try:
            documento = db.session.get(Documento, documento_id)
            if not documento:
                return None
            db.session.delete(documento)
            db.session.commit()
            return DocumentoSchema().dump(documento)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo eliminar el documento: {str(e)}")
