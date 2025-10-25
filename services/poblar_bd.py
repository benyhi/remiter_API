from app import app
import random
from datetime import date, datetime
from faker import Faker
from models.database import db
from models.models import Cliente, Proveedor, Documento, Factura, Pago, NotaCredito, CtaCte, Remito

fake = Faker()

with app.app_context():
# Limpiar tablas antes de poblar (opcional)
    def clear_all():
        db.session.query(CtaCte).delete()
        db.session.query(Factura).delete()
        db.session.query(Pago).delete()
        db.session.query(NotaCredito).delete()
        db.session.query(Documento).delete()
        db.session.query(Remito).delete()
        db.session.query(Cliente).delete()
        db.session.query(Proveedor).delete()
        db.session.commit()

    clear_all()

    # Crear 50 clientes
    clientes = []
    for _ in range(50):
        c = Cliente(
            nombre=fake.name(),
            cuit=fake.unique.ssn()[:11],
            telefono=fake.phone_number()[:10]
        )
        clientes.append(c)
        db.session.add(c)

    # Crear 20 proveedores (menos que clientes para reflejar realidad)
    proveedores = []
    for _ in range(20):
        p = Proveedor(
            nombre=fake.company(),
            cuit=fake.unique.bothify('30#########'),
            telefono=fake.phone_number(),
            email=fake.company_email(),
            direccion=fake.address()
        )
        proveedores.append(p)
        db.session.add(p)

    db.session.commit()  # Necesario para IDs

    # Crear documentos por proveedor (3-8 documentos cada uno)
    documentos = []
    for proveedor in proveedores:
        num_docs = random.randint(20, 50)
        saldo_proveedor = 0
        for _ in range(num_docs):
            doc_tipo = random.choices(["factura", "pago", "nc"], weights=[0.5,0.3,0.2])[0]
            monto = round(random.uniform(100, 5000), 2)
            fecha_doc = fake.date_between(start_date='-1y', end_date='today')

            if isinstance(fecha_doc, str):
                fecha_doc = datetime.strptime(fecha_doc, "%Y-%m-%d").date()

            doc = Documento(
                proveedor_id=proveedor.id,
                tipo=doc_tipo,
                fecha=fecha_doc,
                monto=monto,
                descripcion=fake.sentence()
            )
            db.session.add(doc)
            db.session.flush()  # Para obtener doc.id

            # CtaCte coherente
            debe = monto if doc_tipo == "factura" else 0
            haber = monto if doc_tipo in ["pago", "nc"] else 0
            saldo_proveedor += (debe - haber)
            cta = CtaCte(
                proveedor_id=proveedor.id,
                documento_id=doc.id,
                fecha=fecha_doc,
                descripcion=f"Movimiento {doc_tipo}",
                debe=debe,
                haber=haber,
                saldo=round(saldo_proveedor, 2)
            )
            db.session.add(cta)

            # Tipo de documento
            if doc_tipo == "factura":
                f = Factura(
                    numero=fake.unique.bothify('F-#####'),
                    documento_id=doc.id
                )
                db.session.add(f)
            elif doc_tipo == "pago":
                p = Pago(
                    numero=fake.unique.bothify('P-#####'),
                    documento_id=doc.id,
                    metodo_pago=random.choice(["efectivo", "transferencia", "tarjeta"])
                )
                db.session.add(p)
            elif doc_tipo == "nc":
                nc = NotaCredito(
                    numero=fake.unique.bothify('NC-#####'),
                    documento_id=doc.id
                )
                db.session.add(nc)

            documentos.append(doc)

    db.session.commit()

    # Crear remitos por cliente (2-6 remitos cada uno)
    for cliente in clientes:
        num_remitos = random.randint(2, 6)
        for _ in range(num_remitos):
            productos = [
                {"producto": fake.word(), "cantidad": random.randint(1, 10), "precio": round(random.uniform(50, 500),2)}
                for _ in range(random.randint(1,5))
            ]
            total = round(sum(item["cantidad"] * item["precio"] for item in productos),2)
            
            remito = Remito(
                numero=Remito.get_remito_number(),
                cliente_id=cliente.id,
                fecha=fake.date_between(start_date='-1y', end_date='today'),
                productos=productos,
                total=total
            )
            db.session.add(remito)

    db.session.commit()

    print("✅ Datos de prueba realistas creados:")
    print(f"Clientes: {len(clientes)}, Proveedores: {len(proveedores)}, Documentos: {len(documentos)}")

