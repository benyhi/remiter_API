from models.models import Remito, Cliente
from models.schemas import RemitoSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from services.pdf_service_weasy import PDF
from datetime import datetime
from flask import make_response

class RemitoController:

    @staticmethod
    def get_all():
        try:
            remitos = Remito.query.order_by(Remito.fecha.desc()).all()
            return RemitoSchema(many=True).dump(remitos), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudieron obtener los remitos", "details": str(e)}, 500

    @staticmethod
    def get_one(remito_id):
        try:
            remito = Remito.query.get(remito_id)
            if not remito:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404
            return RemitoSchema().dump(remito), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo obtener el remito", "details": str(e)}, 500

    @staticmethod
    def create(data):
        try:
            cliente_data = data.get("cliente", {})
            productos = data.get("productos")
            total = data.get("total")

            if not productos or total is None:
                return {"error": "Datos incompletos"}, 400

            cliente_id = cliente_data.get("id")
            cliente = None

            if cliente_id and cliente_id != 0:
                cliente = Cliente.query.get(cliente_id)
                if not cliente:
                    return {"error": "Cliente no encontrado"}, 404
            else:
                cuit = cliente_data.get("cuit")
                if not cuit:
                    return {"error": "Falta el CUIT para crear el cliente"}, 400

                cliente = Cliente.query.filter_by(cuit=cuit).first()
                if not cliente:
                    nombre = cliente_data.get("nombre")
                    telefono = cliente_data.get("telefono")
                    if not nombre or not telefono:
                        return {"error": "Datos insuficientes para crear el cliente"}, 400
                    cliente = Cliente(nombre=nombre, cuit=cuit, telefono=telefono)
                    db.session.add(cliente)
                    db.session.commit()

            numero_remito = Remito.get_remito_number()
            remito = Remito(
                cliente_id=cliente.id,
                numero=numero_remito,
                productos=productos,
                total=total
            )
            db.session.add(remito)
            db.session.commit()
    
            return RemitoSchema().dump(remito)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo crear el remito", "details": str(e)}, 500

    @staticmethod
    def update(remito_id, data):
        try:
            remito = Remito.query.get(remito_id)
            if not remito:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404

            if "productos" in data:
                productos = data["productos"]
                if not isinstance(productos, list):
                    return {"error": "El campo 'productos' debe ser una lista"}, 400

                for producto in productos:
                    if not all(k in producto for k in ("cantidad", "descripcion", "precio", "subtotal")):
                        return {"error": "Faltan datos en uno o más productos"}, 400

                remito.productos = productos
                remito.total = sum(float(p["subtotal"]) for p in productos)

            elif "total" in data:
                remito.total = data["total"]

            db.session.commit()
            return {
                "message": "Remito actualizado con éxito",
                "remito_actualizado": RemitoSchema().dump(remito)
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo actualizar el remito", "details": str(e)}, 500

    @staticmethod
    def delete(remito_id):
        try:
            remito = Remito.query.get(remito_id)
            if not remito:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404

            db.session.delete(remito)
            db.session.commit()

            return {
                "message": "Remito eliminado con éxito",
                "remito_eliminado": RemitoSchema().dump(remito)
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo eliminar el remito", "details": str(e)}, 500

    @staticmethod
    def generate_pdf(data):
        if data:
            try: 
                # LLama a la funcion para crear el PDF
                pdf = PDF.generate_pdf_weasy(data)

                # Crear la respuesta con el PDF generado
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

                return response, 200

            except Exception as e:
                print(f"❌ Error al generar PDF: {e}")
                return {"error": "Error inesperado"}, 400
        else:
            return {"error": "No hay datos"}, 400

    @staticmethod
    def print_pdf(remito_id):
        remito_response, status = RemitoController.get_one(remito_id)
        if status != 200:
            return remito_response, status

        remito_dict = remito_response.copy()
        fecha_str = remito_dict.get("fecha")

        if fecha_str:
            try:
                fecha_obj = datetime.fromisoformat(fecha_str)
                remito_dict["fecha"] = fecha_obj.strftime("%d/%m/%Y")
            except Exception:
                pass

        for producto in remito_dict.get("productos", []):
            try:
                producto["precio"] = float(producto["precio"])
                producto["cantidad"] = int(producto["cantidad"])
                producto["subtotal"] = float(producto["subtotal"])
            except Exception:
                pass

        remito_dict["total"] = float(remito_dict.get("total", 0))

        pdf = PDF.generate_pdf_weasy(remito_dict)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response
