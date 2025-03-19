from flask import jsonify, render_template, make_response
from models.models import Remito, Cliente
from models.schemas import RemitosSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from services.pdf_service import PDF
from datetime import datetime


class RemitoController:

    @staticmethod #OK
    def get_all():
        try:
            remitos = Remito.query.all()
            remitos_schema = RemitosSchema(many=True)
            return remitos_schema.dump(remitos)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudieron obtener los remitos", "details": str(e)}, 500

    @staticmethod #OK
    def get_one(remito_id):
        try:
            remito = Remito.query.get(remito_id)
            if remito is None:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404

            remito_schema = RemitosSchema()
            return remito_schema.dump(remito)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo obtener el remito", "details": str(e)}, 500

    @staticmethod #OK
    def create(data):
        try:
            cuit = data.get("cuit")
            productos = data.get("productos")
            total = data.get("total")

            if not cuit or not productos or total is None:
                return {"error": "Datos incompletos"}, 400

            cliente = Cliente.query.filter_by(cuit=cuit).first()

            if not cliente:
                nombre = data.get("nombre")
                telefono = data.get("telefono")

                if nombre and telefono:
                    try:
                        nuevo_cliente = Cliente(
                            nombre=nombre,
                            cuit=cuit,
                            telefono=telefono
                        )
                        db.session.add(nuevo_cliente)
                        db.session.commit()
                        cliente = nuevo_cliente
                        print(f"🟢Cliente creado con exito {cliente}")

                    except Exception as e:
                        db.session.rollback()
                        return {f"message":"Error al cargar nuevo cliente", "details": str(e)}, 500
                else:     
                    return {"error": "Cliente no encontrado y no se proporcionaron datos para crearlo."}, 404
                
            numero_remito = Remito.get_remito_number()

            remito = Remito(
                cliente_id=cliente.id,
                numero=numero_remito,
                productos=productos,
                total=total
            )

            db.session.add(remito)
            print(f"🟢 Remito agregado a la sesión: {remito}")

            db.session.commit()
            print(f"✅ Commit exitoso. ID del remito: {remito.id}")

            remito_schema = RemitosSchema()
            return {"message": "Remito creado con éxito", "nuevo_remito": remito_schema.dump(remito)}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Error de SQLAlchemy: {e}")
            return {"error": "No se pudo crear el remito", "details": str(e)}, 500 

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            return {"error": "Error inesperado", "details": str(e)}, 500

    @staticmethod
    def update(data):
        try:
            remito_id = data.get("id")
            remito = Remito.query.get(remito_id)
            if remito is None:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404
            
            if "productos" in data:
                productos = data["productos"]

                # Validación para asegurarse de que 'productos' sea una lista de diccionarios
                if isinstance(productos, list):
                    for producto in productos:
                        if not all(k in producto for k in ("cantidad", "descripcion", "precio", "subtotal")): #Validacion para ver que esten todos los campos.
                            return {"error": "Faltan datos en uno o más productos"}, 400
                    remito.productos = productos
                else:
                    return {"error": "El campo 'productos' debe ser una lista"}, 400

            if "total" in data:
                remito.total = data["total"]

            db.session.commit()
            remito_schema = RemitosSchema()

            return {"message": "Remito actualizado con éxito", "remito_actualizado": remito_schema.dump(remito)}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo actualizar el remito", "details": str(e)}, 500

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}, 500

    @staticmethod #OK
    def delete(remito_id):
        try:
            remito = Remito.query.get(remito_id)
            if remito is None:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404

            db.session.delete(remito)
            db.session.commit()

            remito_schema = RemitosSchema()
            return {"message": "Remito eliminado con exito" ,"remito_eliminado": remito_schema.dump(remito)}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo eliminar el remito", "details": str(e)}, 500

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}, 500

    @staticmethod #Optional
    def import_data(file_path):
        try:
            import_excel = ImportExcel(file_path)
            data = import_excel.read_excel()
            remitos = []
            
            for row in data:
                row = {key.lower().replace(" ", "_"): value for key, value in row.items()}

                cliente = row.get('cliente')
                cliente_id = Cliente.query.filter(
                    (Cliente.nombre == cliente) | (Cliente.cuil == cliente)
                ).first()

                if cliente is None:
                    return {"error": f"Cliente {cliente} no encontrado"}, 404

                try:
                    remito = Remito(
                        numero=row.get('numero'),
                        cliente_id=cliente_id.id,
                        fecha=row.get('fecha'),
                        productos=row.get('productos'),
                        total=row.get('total')
                    )
                    remitos.append(remito)

                except SQLAlchemyError as e:
                    db.session.rollback()
                    print (f"Error al importar el cliente {row}")
                    continue

            if remitos:
                db.session.add_all(remitos)
                db.session.commit()
                remito_schema = RemitoSchema(many=True)
                return {"message": "Remitos importados con éxito", "remitos_importados": remito_schema.dump(remitos)}, 200
            else:
                return {"error": "No se pudo importar ningun remito"}, 400

        except Exception as e:
            return {"error": "No se pudo importar los datos", "details": str(e)}, 500

    @staticmethod
    def generate_pdf(data):
        if data:
            try: 
                #Intenta crear el remito
                result, status_code = RemitoController.create(data)

                if status_code != 201:
                    print(f"❌ No se pudo crear el remito: {result}")
                    return {"error": "No se pudo crear el remito", "details": result}, status_code

                print("🟢 Remito creado y guardado con éxito.")

                # LLama a la funcion para crear el PDF
                pdf = PDF.generate(data)

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
