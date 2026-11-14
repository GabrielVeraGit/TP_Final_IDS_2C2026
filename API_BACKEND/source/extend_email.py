import os
from flask_mail import Mail, Message
from errors_code import ERROR_CLIENTE, ERROR_SERVIDOR

mail = Mail()

def config(app):
    app.config['MAIL_SERVER'] = os.getenv("EMAIL_DOMINIO_REMITENTE")
    app.config['MAIL_PORT'] = int(os.getenv("EMAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("EMAIL_REMITENTE")
    app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD_REMITENTE") 
    app.config['MAIL_DEFAULT_SENDER'] = (os.getenv("DB_NAME"), os.getenv("EMAIL_REMITENTE"))

    mail.init_app(app)#resultado igual a mail = Mail(app)

def send_email(asunto:str, destinatarios:list, cuerpo_texto:str):
    try:
        if len(destinatarios)==0:
            return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"No se especificó ningún destinatario")
        
        msg = Message(subject=asunto, recipients=destinatarios, body=cuerpo_texto)
        mail.send(msg)

        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"send_email, motivo: {str(e)}")