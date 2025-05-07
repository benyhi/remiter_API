from flask import render_template, make_response
from xhtml2pdf import pisa
import io

class PDF():

    @staticmethod
    def generate(data):
        try:
            html = render_template('remito.html', **data)
            
            # Crear un buffer en memoria para almacenar el PDF
            with io.BytesIO() as pdf_buffer:
                pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf-8')), pdf_buffer)
                if pdf.err:
                    print("❌ Error en pisa:", pdf.err)
                    return None
                
                return pdf_buffer.getvalue()
            
        except Exception as e:
            print("❌ Error al generar el PDF:", str(e))
            return None
