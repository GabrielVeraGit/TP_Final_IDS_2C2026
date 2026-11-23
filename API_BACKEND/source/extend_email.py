import os
from flask_mail import Mail, Message
from errors_code import ERROR_CLIENTE, ERROR_SERVIDOR
from flask import render_template

mail = Mail()

def config(app):
    app.config['MAIL_SERVER'] = os.getenv("EMAIL_DOMINIO_REMITENTE")
    app.config['MAIL_PORT'] = int(os.getenv("EMAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("EMAIL_REMITENTE")
    app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD_REMITENTE") 
    app.config['MAIL_DEFAULT_SENDER'] = (os.getenv("DB_NAME"), os.getenv("EMAIL_REMITENTE"))

    mail.init_app(app)#resultado igual a mail = Mail(app)

def send_bienvenida(usr:dict):
    try:

        msg = Message(subject=f"Bienvenido/a, gracias por registrarse", recipients=[usr["email"],])
        msg.html=render_template('bienvenida.html',
                                 nombre=usr["nombre"],
                                 apellido=usr["apellido"],
                                 usuario=usr["email"],
                                 rol=usr["rol"])

        mail.send(msg)

        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"send_email, motivo: {str(e)}")


def send_reserva(qr_id:str, url_cancelar:str, qr_buffer, identificador:str, registro:dict):
    try:
        
        msg = Message(subject=f"Reserva exitosa", recipients=[identificador,])

        msg.html=render_template('reserva.html',
                                qr=qr_id, 
                                cancelar_url_boton=url_cancelar, 
                                fecha_funcion=registro["fecha_hora"], 
                                sala=registro["name_sala"], 
                                sede=registro["name_sede"],
                                direccion=registro["direccion_sede"],
                                cant_entradas=registro["cant_entradas"] )

        msg.attach(
                    filename=f"{qr_id}.png",
                    content_type="image/png",
                    data=qr_buffer.read(),
                    disposition="inline",
                    headers={'Content-ID': '<qr_reserva>'})               
        mail.send(msg)

        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"send_email, motivo: {str(e)}")