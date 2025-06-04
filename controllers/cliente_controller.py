from models.models import Cliente
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from models.schemas import ClienteSchema
from models.database import db

class ClienteController:

    @staticmethod
    def get_all():
        try:
            clientes = Cliente.query.order_by(func.lower(Cliente.nombre)).all()
            cliente_schema = ClienteSchema(many=True)
            return cliente_schema.dump(clientes)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los clientes: {e}")

    @staticmethod
    def get_one(cliente_id):
        try:
            cliente = Cliente.query.get(cliente_id)
            if cliente is None:
                return None
            cliente_schema = ClienteSchema()
            return cliente_schema.dump(cliente)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo obtener el cliente: {e}")

    @staticmethod
    def create(data):
        try:
            cliente = Cliente(**data)
            db.session.add(cliente)
            db.session.commit()
            cliente_schema = ClienteSchema()
            return cliente_schema.dump(cliente)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo crear el cliente: {e}")

    @staticmethod
    def update(data):
        try:
            cliente_id = data.get("id")
            cliente = Cliente.query.get(cliente_id)
            if cliente is None:
                return None
            for key, value in data.items():
                if hasattr(cliente, key):
                    setattr(cliente, key, value)
            db.session.commit()
            cliente_schema = ClienteSchema()
            return cliente_schema.dump(cliente)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo actualizar el cliente: {e}")

    @staticmethod
    def delete(cliente_id):
        try:
            cliente = Cliente.query.get(cliente_id)
            if cliente is None:
                return None
            db.session.delete(cliente)
            db.session.commit()
            cliente_schema = ClienteSchema()
            return cliente_schema.dump(cliente)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo eliminar el cliente: {e}")
