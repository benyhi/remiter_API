from weasyprint import HTML, CSS
from flask import render_template, current_app
import io
import os
import math
import copy

class PDF:

    @staticmethod
    def fill_rows(items, total_rows=14):
        while len(items) < total_rows:
            items.append({
                "cantidad": "",
                "descripcion": "",
                "precio": "",
                "subtotal": ""
            })
        return items

    @staticmethod
    def generate_pdf_weasy(data):
        """
        - data["productos"]: lista de dicts con {cantidad, descripcion, precio, subtotal}.
        - data también trae {cliente, fecha, numero, direccion, …} que se usan en el template R_A4_OyD.html.
        - Si hay más de 13 productos, se van a crear tantas páginas (trozos) como hagan falta.
        - Luego se concatena todo el HTML y WeasyPrint genera un único PDF multi‐página.
        """
        productos = data.get("productos", [])
        filas_por_pagina = 13

        # 1) Si hay <=13, solo se renderiza un unico bloque y si faltan productos para llegar a los 13
        # se autocompletan llamando a fill_rows().

        if len(productos) <= filas_por_pagina:
            data["productos"] = PDF.fill_rows(productos.copy(), filas_por_pagina)
            html_content = render_template('R_A4_OyD.html', **data)
            css_path = os.path.join(current_app.root_path, 'static', 'remito.css')

            try:
                return PDF.generate_pdf_from_html(html_content, css_path)
            
            except Exception as e:
                return {"error": "Error al generar el PDF"}

        # 2) Si hay >13, hay que dividir los productos en bloques para generar tantas páginas como sea necesario.
        else:
            total_productos = len(productos)
            total_paginas = math.ceil(total_productos / filas_por_pagina) #math.ceil() si hay decimales redondea hacia arriba
            # Vamos a concatenar N bloques de HTML (uno por página)
            html_completo = ""

            # Hacemos una copia de “data” para no pisar la lista original
            datos_base = copy.deepcopy(data)
            css_path = os.path.join(current_app.root_path, 'static', 'remito.css')

            for i in range(total_paginas):
                inicio = i * filas_por_pagina
                fin = inicio + filas_por_pagina
                bloque = productos[inicio:fin]

                bloque = PDF.fill_rows(bloque.copy(), filas_por_pagina)

                # Para no mutar la lista original, armamos un nuevo dict “datos_pagina”
                datos_pagina = {
                    **datos_base,
                    "productos": bloque,
                    "pagina_actual": i + 1,
                    "total_paginas": total_paginas
                }

                # Renderizamos un solo “bloque” de HTML que produce EXACTAMENTE una página
                # (R_A4_OyD.html debe estar armado para aceptar {{productos}}, {{pagina_actual}}, {{total_paginas}}, etc.)
                bloque_html = render_template('R_A4_OyD.html', **datos_pagina)

                # IMPORTANTE: Asumimos que R_A4_OyD.html envuelve su contenido en
                # <div class="page">…</div> con CSS `page-break-after: always;`
                # de modo que WeasyPrint sepa dónde forzar salto de página.
                
                html_completo += bloque_html

            # 3) Una sola llamada final a WeasyPrint con todo el HTML concatenado

            try:
                return PDF.generate_pdf_from_html(html_completo, css_path)
            
            except Exception as e:
                return {"error": f"Error al generar el PDF {e}"}

    @staticmethod
    def generate_pdf_from_html(html_content, css_path=None):
        """
        Genera un PDF a partir de un string HTML y una ruta opcional de CSS.
        """
        try:
            base_url = current_app.root_path if current_app else None
            with io.BytesIO() as pdf_buffer:
                HTML(string=html_content, base_url=base_url).write_pdf(
                    target=pdf_buffer,
                    stylesheets=[CSS(filename=css_path)] if css_path else []
                )
                return pdf_buffer.getvalue()
            
        except Exception as e:
            return {"error": f"Error al generar el PDF {e}"}