import os
from datetime import timedelta
from flask import jsonify
from errors_code import ERROR_CLIENTE
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity, get_jwt #tokens
jwt = JWTManager()

def crear_token(registro:dict)->str: #registro tiene TODA la info del usuario
    data_extra={"id_usuario":registro["id_usuario"], 
                "email":registro["email"], 
                "rol":registro["rol"]}
    # identity ----------- (obligatorio) el duenio del token str()
    # expires_delta ------ tiempo de expiracion 15 deafult
    # additional_claims -- diccionario con datos extra!! ej id_user, email, rol
    token = create_access_token(identity=registro["email"], additional_claims=data_extra)
    return token

def crear_cookie(token:str):
    respuesta = jsonify({"login": True})
    set_access_cookies(response=respuesta, encoded_access_token=token)
    return respuesta

def eliminar_cookie(respuesta=None):
    if respuesta is None:
        respuesta = jsonify({"logout": True})
    unset_jwt_cookies(response=respuesta)
    return respuesta

def obtener_informacion_token():
    identificador = get_jwt_identity()
    data_extra = get_jwt()
    return identificador, data_extra

def config(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("PASSWORD_REMITENTE") #clave super secreta
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"] #enves de leer y enviar tokens, seran cookies
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)#tiempo de duracion de la cookie
    
    jwt.init_app(app)#resultado igual a jwt = JWTManager(app)


#ERRORS ENPOINTS JWT
@jwt.expired_token_loader
def token_expirado(jwt_header, jwt_payload):
    json, code_n = ERROR_CLIENTE["UNAUTHORIZED"]("Token caducado, por favor inicia sesión nuevamente.")
    respuesta = eliminar_cookie(json)
    return respuesta, code_n

@jwt.unauthorized_loader
def token_ausente(reason):
    return ERROR_CLIENTE["UNAUTHORIZED"]("No se mando un token")