from weasyprint import HTML, CSS
from flask import render_template, current_app
import io
import os

class PDF():

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
        if len(data["productos"]) < 12:
            data["productos"] = PDF.fill_rows(data["productos"], 12)

        try: 
            html_content = render_template('R_A4_OyD.html', **data)

            # Ruta correcta al CSS (carpeta static en raíz del proyecto)
            css_path = os.path.join(current_app.root_path, 'static', 'remito.css')
            
            # Directorio base para que WeasyPrint resuelva rutas relativas a imágenes
            base_url = os.path.join(current_app.root_path)

            # Crear PDF en memoria
            with io.BytesIO() as pdf_buffer:
                HTML(string=html_content, base_url=base_url).write_pdf(
                    target=pdf_buffer,
                    stylesheets=[CSS(filename=css_path)]
                )
                pdf_data = pdf_buffer.getvalue()
                return pdf_data
        
        except Exception as e:
            print(f"❌ Error al generar el PDF: {e}")
            return {"error": "Error al generar el PDF"}, 500
        
