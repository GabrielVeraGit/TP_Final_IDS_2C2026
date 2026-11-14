from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity, get_jwt #tokens

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