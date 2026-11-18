import os
from datetime import timedelta
from flask_jwt_extended import (JWTManager, jwt_required,
    unset_jwt_cookies,
    get_jwt_identity, 
    get_jwt) #tokens
from flask import redirect, url_for

jwt = JWTManager()

seguro = jwt_required

def obtener_informacion_token():
    identificador = get_jwt_identity() #si no hay cokie retorna None
    data_extra = get_jwt()
    return identificador, data_extra

def config(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("TOKEN_KEY_CODIFICACION") #clave super secreta
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"] #enves de leer y enviar tokens, seran cookies
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    
    jwt.init_app(app)#resultado igual a jwt = JWTManager(app)

def verificar_rol_permitido(rol_permitido:str):
    identificador, data_extra = obtener_informacion_token()
    if data_extra["rol"] == rol_permitido:
        return False, None
    return True, f"Usted no es {rol_permitido}"

def eliminar_cookie(resp):
    unset_jwt_cookies(resp)
    return resp

#ERRORS ENPOINTS JWT
@jwt.expired_token_loader
def token_expirado(jwt_header, jwt_payload):
    return redirect(url_for('login'))

@jwt.unauthorized_loader
def token_ausente(reason):
    return redirect(url_for('login'))