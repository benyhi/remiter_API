from sqlalchemy import event
from sqlalchemy.orm import Session
from models.models import Pago, Factura

@event.listens_for(Session, "after_flush")
def actualizar_facturas_con_pagos(session, context):
    # Reviso los objetos modificados en esta transacción
    for obj in session.new.union(session.dirty).union(session.deleted):
        if isinstance(obj, Pago):
            # Si el pago se eliminó puede que target.factura no exista → buscamos por id
            factura = obj.factura or (session.get(Factura, obj.factura_id) if obj.factura_id else None)
            if factura:
                factura.actualizar_estado()