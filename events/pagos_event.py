from sqlalchemy import event, inspect, func
from sqlalchemy.orm import Session
from models.models import Pago, Factura

@event.listens_for(Session, "before_flush")
def pagos_before_flush(session: Session, flush_context, instances):
    """
    Recolecta facturas afectadas por cambios en Pago antes de que se haga flush.
    Guarda los ids en session.info para usarlos después.
    """
    factura_ids = session.info.setdefault("facturas_afectadas", set())

    # nuevos
    for obj in list(session.new):
        if isinstance(obj, Pago) and getattr(obj, "factura_id", None):
            factura_ids.add(obj.factura_id)

    # modificados
    for obj in list(session.dirty):
        if not isinstance(obj, Pago):
            continue
        insp = inspect(obj)
        hist = insp.attrs.factura_id.history
        if hist.deleted:
            old_id = hist.deleted[0]
            if old_id:
                factura_ids.add(old_id)
        if hist.added:
            new_id = hist.added[0]
            if new_id:
                factura_ids.add(new_id)
        # si no cambió la fk, recalculamos la actual (si existe)
        if not hist.added and not hist.deleted and getattr(obj, "factura_id", None):
            factura_ids.add(obj.factura_id)

    # eliminados
    for obj in list(session.deleted):
        if isinstance(obj, Pago) and getattr(obj, "factura_id", None):
            factura_ids.add(obj.factura_id)


@event.listens_for(Session, "after_flush_postexec")
def pagos_after_flush_postexec(session: Session, ctx):
    """
    Recalcula el estado de las facturas cuyo id se guardó en session.info['facturas_afectadas'].
    """
    factura_ids = session.info.pop("facturas_afectadas", None)
    if not factura_ids:
        return

    for fid in factura_ids:
        try:
            factura = session.get(Factura, fid)
            if not factura:
                continue

            total_db = session.query(func.coalesce(func.sum(Pago.monto_pagado), 0.0))\
                .filter(Pago.factura_id == fid).scalar() or 0.0

            factura.actualizar_estado(session=session)

            session.add(factura)
        except Exception:
            pass
