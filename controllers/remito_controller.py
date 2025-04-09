from flask import jsonify, render_template, make_response
from models.models import Remito, Cliente
from models.schemas import RemitoSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError
from services.pdf_service import PDF
from datetime import date, datetime


class RemitoController:

    @staticmethod #OK
    def get_all():
        try:
            remitos = Remito.query.order_by(Remito.fecha.desc()).all()
            remitos_schema = RemitoSchema(many=True)
            return remitos_schema.dump(remitos)

        except Exception as e:
                    print(f"⚠️ Error inesperado: {e}")
                    return {"error": "Error inesperado", "details": str(e)}, 500

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudieron obtener los remitos", "details": str(e)}, 500

    @staticmethod #OK
    def get_one(remito_id):
    #Obtiene el remito por id
        try:
            remito = Remito.query.get(remito_id)
            if remito is None:
                return {"error": f"Remito con id {remito_id} no encontrado"}, 404

            remito_schema = RemitoSchema()
            return remito_schema.dump(remito)

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            return {"error": "Error inesperado", "details": str(e)}, 500

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo obtener el remito", "details": str(e)}, 500

    @staticmethod
    def create(data):
        print("➡️ Iniciando creación de remito")
        print(f"📦 Datos recibidos: {data}")
        
        try:
            cliente_data = data.get("cliente", {})
            cliente_id = cliente_data.get("id")
            productos = data.get("productos")
            total = data.get("total")

            print(f"🧾 Cliente ID: {cliente_id}, Total: {total}, Productos: {productos}")

            if not productos or total is None:
                print("❌ Faltan productos o total")
                return {"error": "Datos incompletos"}, 400

            cliente = None

            # Si viene cliente_id válido (distinto de None o 0)
            if cliente_id and cliente_id != 0:
                print("🔍 Buscando cliente existente por ID")
                cliente = Cliente.query.get(cliente_id)
                if not cliente:
                    print("❌ Cliente no encontrado por ID")
                    return {"error": "Cliente no encontrado"}, 404
                print(f"✅ Cliente encontrado: {cliente}")

            else:
                print("➕ Creando o buscando cliente por CUIT")
                cuit = cliente_data.get("cuit")
                if not cuit:
                    print("❌ CUIT faltante")
                    return {"error": "Falta el CUIT para crear el cliente"}, 400

                cliente = Cliente.query.filter_by(cuit=cuit).first()
                if not cliente:
                    nombre = cliente_data.get("nombre")
                    telefono = cliente_data.get("telefono")

                    if not nombre or not telefono:
                        print("❌ Nombre o teléfono faltante para crear cliente")
                        return {"error": "Datos insuficientes para crear el cliente"}, 400

                    try:
                        nuevo_cliente = Cliente(nombre=nombre, cuit=cuit, telefono=telefono)
                        db.session.add(nuevo_cliente)
                        db.session.commit()
                        cliente = nuevo_cliente
                        print(f"🟢 Cliente creado con éxito: {cliente}")
                    except Exception as e:
                        db.session.rollback()
                        print(f"❌ Error al crear cliente: {e}")
                        return {"message": "Error al cargar nuevo cliente", "details": str(e)}, 500
                else:
                    print(f"📌 Cliente ya existente: {cliente}")

            numero_remito = Remito.get_remito_number()
            print(f"🧾 Número de remito generado: {numero_remito}")

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

            remito_schema = RemitoSchema()
            resultado = remito_schema.dump(remito)
            print(f"🟢 Remito creado: {resultado}")

            return {"message": "Remito creado con éxito", "nuevo_remito": resultado}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Error de SQLAlchemy: {e}")
            return {"error": "No se pudo crear el remito", "details": str(e)}, 500

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            return {"error": "Error inesperado", "details": str(e)}, 500


    @staticmethod
    def update(id, data):
        try:
            remito_id = id
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

                    remito.total = sum(float(p["subtotal"]) for p in productos) # Actualiza el total sumando los subtotales de los productos
                else:
                    return {"error": "El campo 'productos' debe ser una lista"}, 400

            elif "total" in data:
                remito.total = data["total"]

            db.session.commit()
            remito_schema = RemitoSchema()

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

            remito_schema = RemitoSchema()
            return {"message": "Remito eliminado con exito" ,"remito_eliminado": remito_schema.dump(remito)}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo eliminar el remito", "details": str(e)}, 500

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}, 500

    # @staticmethod #Optional
    # def import_data(file_path):
    #     try:
    #         import_excel = ImportExcel(file_path)
    #         data = import_excel.read_excel()
    #         remitos = []
            
    #         for row in data:
    #             row = {key.lower().replace(" ", "_"): value for key, value in row.items()}

    #             cliente = row.get('cliente')
    #             cliente_id = Cliente.query.filter(
    #                 (Cliente.nombre == cliente) | (Cliente.cuil == cliente)
    #             ).first()

    #             if cliente is None:
    #                 return {"error": f"Cliente {cliente} no encontrado"}, 404

    #             try:
    #                 remito = Remito(
    #                     numero=row.get('numero'),
    #                     cliente_id=cliente_id.id,
    #                     fecha=row.get('fecha'),
    #                     productos=row.get('productos'),
    #                     total=row.get('total')
    #                 )
    #                 remitos.append(remito)

    #             except SQLAlchemyError as e:
    #                 db.session.rollback()
    #                 print (f"Error al importar el cliente {row}")
    #                 continue

    #         if remitos:
    #             db.session.add_all(remitos)
    #             db.session.commit()
    #             remito_schema = RemitoSchema(many=True)
    #             return {"message": "Remitos importados con éxito", "remitos_importados": remito_schema.dump(remitos)}, 200
    #         else:
    #             return {"error": "No se pudo importar ningun remito"}, 400

    #     except Exception as e:
    #         return {"error": "No se pudo importar los datos", "details": str(e)}, 500

    @staticmethod
    def generate_pdf(data):
        if data:
            try: 
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

    @staticmethod
    def print_pdf(id):
        remito = RemitoController.get_one(id)
        if remito:
            try:
                remito_dict = remito.copy()

                fecha_str = remito_dict.get("fecha")
                if fecha_str:
                    try:
                        fecha_obj = datetime.fromisoformat(fecha_str)
                        remito_dict["fecha"] = fecha_obj.strftime("%d/%m/%Y")
                        print(f"📅 Fecha formateada: {remito_dict['fecha']}")
                    except Exception as e:
                        print(f"⚠️ Error al convertir la fecha: {e}")

                # Conversión de tipos para evitar errores en cálculos
                for producto in remito_dict.get("productos", []):
                    try:
                        producto["precio"] = float(producto["precio"])
                        producto["cantidad"] = int(producto["cantidad"])
                        producto["subtotal"] = float(producto["subtotal"])
                    except Exception as e:
                        print(f"⚠️ Error al convertir tipos en producto: {producto} - {e}")

                remito_dict["total"] = float(remito_dict.get("total", 0))

                pdf = PDF.generate(remito_dict)
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
                return response, 200

            except Exception as e:
                print(f"❌ Error al generar PDF: {e}")
                return {"error": "Error inesperado"}, 400
        else:
            return {"error": "No hay datos"}, 400

