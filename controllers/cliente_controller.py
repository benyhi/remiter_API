from models.models import Cliente
from sqlalchemy.exc import SQLAlchemyError
from models.schemas import ClienteSchema
from models.database import db
from services.import_excel import ImportExcel

class ClienteController:
    
    @staticmethod
    def get_all():
        try:
            clientes = Cliente.query.all()
            cliente_schema = ClienteSchema(many=True)
            return cliente_schema.dump(clientes)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudieron obtener los clientes", "details": str(e)}, 500
        

    @staticmethod
    def get_one(cliente_id):
        try:     
            cliente = Cliente.query.get(cliente_id)
            if cliente is None:
                return {"error": "Cliente no encontrado"}, 404

            cliente_schema = ClienteSchema()
            return cliente_schema.dump(cliente)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo obtener el cliente", "details": str(e)}, 500


    @staticmethod
    def create(data):
        try:
            cliente = Cliente(**data)
            db.session.add(cliente)
            db.session.commit()

            cliente_schema = ClienteSchema()
            return {"message": "Cliente cargado con exito", "nuevo_cliente": cliente_schema.dump(cliente)}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo crear el cliente", "details": str(e)}, 500

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}, 500
    
    @staticmethod
    def update(data):
        try:
            cliente_id = data.get("id")
            cliente = Cliente.query.get(cliente_id)
            if cliente is None:
                return {"error": "Cliente no encontrado"}, 404

            for key, value in data.items():
                setattr(cliente, key, value)

            db.session.commit()
            cliente_schema = ClienteSchema()

            return {"message": "Cliente actualizado con exito", "cliente_actualizado": cliente_schema.dump(cliente)}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "No se pudo actualizar el cliente", "details": str(e)}, 500

        except Exception as e:
            return {"error": "Error inesperado", "details": str(e)}, 500

    @staticmethod
    def delete(cliente_id):
        try:
            cliente = Cliente.query.get(cliente_id)
            if not cliente:
                print(f"Cliente con ID {cliente_id} no encontrado")  # Depuración
                return {"error": "Cliente no encontrado"}, 404  

            print(f"Eliminando cliente: {cliente}")  # Depuración
            db.session.delete(cliente)
            db.session.commit()
            print(f"Cliente {cliente_id} eliminado con éxito")  # Depuración

            cliente_schema = ClienteSchema()
            return {"message": "Cliente eliminado con éxito", "cliente_eliminado": cliente_schema.dump(cliente)}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error SQL: {e}")  # Depuración
            return {"error": "No se pudo eliminar el cliente", "details": str(e)}, 500

        except Exception as e:
            print(f"Error inesperado: {e}")  # Depuración
            return {"error": "Error inesperado", "details": str(e)}, 500


    @staticmethod
    def import_data(file_path):
        try:
            import_excel = ImportExcel(file_path)
            data = import_excel.read_excel()
            clientes = []
            
            for row in data:
                row = {key.lower().replace(" ", "_"): value for key, value in row.items()}
                
                try:
                    cliente = Cliente(**row)
                    clientes.append(cliente)

                except SQLAlchemyError as e:
                    db.session.rollback()
                    print (f"Error al importar el cliente {row}")
                    continue

            if clientes:
                db.session.add_all(clientes)
                db.session.commit()
                cliente_schema = ClienteSchema(many=True)
                return {"message": "Clientes importados con exito", "clientes_importados": cliente_schema.dump(clientes)}, 200
            else:
                return {"error": "No se pudo importar ningun cliente"}, 400
        
        except Exception as e:
            return {"error": "No se pudo importar los datos", "details": str(e)}, 500