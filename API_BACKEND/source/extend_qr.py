import io
import uuid
import qrcode
import os
from flask import request

def generar_qr_en_memoria(contenido_url: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(contenido_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0) 
    return buffer



def generar_code_y_urls():
    qr_id = f"QR_ID-{uuid.uuid4().hex[:10].upper()}"

    protocolo = request.scheme                      # 'http'
    host, port_back = request.host.split(':')        # '127.0.0.1:5001'
    port_front=os.getenv("PORT_APLICATIVO_FRONTEND")

    url_usar=f"{protocolo}://{host}:{port_back}/api/reserva/{qr_id}/usar" #va al qr
    url_cancelar=f"{protocolo}://{host}:{port_back}/api/reserva/{qr_id}/cancelar" #va al boton
    
    return qr_id, url_usar, url_cancelar