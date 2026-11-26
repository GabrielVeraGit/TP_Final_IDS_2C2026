import io
import base64
import uuid
import qrcode
from source.utils import config



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

def generar_qr_base64(contenido_url: str):
    buffer = generar_qr_en_memoria(contenido_url)
    return base64.b64encode(buffer.read()).decode("utf-8")

def generar_qr_id():
    return f"QR_ID-{uuid.uuid4().hex[:10].upper()}"

def armar_urls(qr_id: str):
    url_usar = f"{config.URL_FRONTEND}/reservas/{qr_id}/usar" #va al qr de la entrada
    url_cancelar = f"{config.URL_FRONTEND}/reservas/{qr_id}/cancelar" #va al boton
    url_pagar = f"{config.URL_FRONTEND}/reservas/{qr_id}/pagar" #va al qr de pago

    return url_usar, url_cancelar, url_pagar

