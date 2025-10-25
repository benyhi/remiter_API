from models.models import Proveedor
from models.schemas import ProveedorSchema, ProveedorNomSchema
from models.database import db
from sqlalchemy.exc import SQLAlchemyError

class ProveedorController:
    """Controlador de proveedores"""

    # --- LISTAR TODOS LOS PROVEEDORES (modo liviano) ---
    @staticmethod
    def get_all():
        try:
            proveedores = Proveedor.query.order_by(Proveedor.nombre.asc()).all()
            return proveedores  # devolvemos objetos, no JSON
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudieron obtener los proveedores: {str(e)}")

    # --- OBTENER UN PROVEEDOR CON DETALLE ---
    @staticmethod
    def get_one(proveedor_id):
        try:
            proveedor = db.session.get(Proveedor, proveedor_id)
            if not proveedor:
                return None
            return proveedor
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo obtener el proveedor: {str(e)}")

    # --- CREAR UN NUEVO PROVEEDOR ---
    @staticmethod
    def create(data):
        try:
            nombre = data.get("nombre")
            cuit = data.get("cuit")
            telefono = data.get("telefono")
            email = data.get("email")
            direccion = data.get("direccion")

            if not nombre or not cuit:
                raise Exception("Datos incompletos para crear el proveedor")

            proveedor = Proveedor(
                nombre=nombre,
                cuit=cuit,
                telefono=telefono,
                email=email,
                direccion=direccion
            )
            db.session.add(proveedor)
            db.session.commit()
            return proveedor
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo crear el proveedor: {str(e)}")

    # --- ACTUALIZAR UN PROVEEDOR EXISTENTE ---
    @staticmethod
    def update(proveedor_id, data):
        try:
            proveedor = db.session.get(Proveedor, proveedor_id)
            if not proveedor:
                return None

            for key in ["nombre", "cuit", "telefono", "email", "direccion"]:
                if key in data:
                    setattr(proveedor, key, data[key])

            db.session.commit()
            return proveedor
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo actualizar el proveedor: {str(e)}")

    # --- ELIMINAR UN PROVEEDOR ---
    @staticmethod
    def delete(proveedor_id):
        try:
            proveedor = db.session.get(Proveedor, proveedor_id)
            if not proveedor:
                return None

            db.session.delete(proveedor)
            db.session.commit()
            return {"message": f"Proveedor {proveedor.nombre} eliminado correctamente"}
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"No se pudo eliminar el proveedor: {str(e)}")
