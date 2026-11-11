from flask import current_app
from flask_mail import Message
from errors_code import ERROR_CLIENTE, ERROR_SERVIDOR

def send_email(asunto:str, destinatarios:list, cuerpo_texto:str):
    try:
        from app import mail

        if len(destinatarios)==0:
            return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"No se especificó ningún destinatario")
        mensaje = Message(
        subject=asunto,
        recipients=destinatarios
        )
        mensaje.body = cuerpo_texto

        with current_app.app_context():
            mail.send(mensaje)

        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"send_email, motivo: {str(e)}")