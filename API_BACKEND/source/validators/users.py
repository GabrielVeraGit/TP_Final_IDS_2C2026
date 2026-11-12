from flask import request
from errors_code import ERROR_CLIENTE
from source.utils.validaciones import validar_body_json, validar_texto, validar_email



def validando_solo_letras(campo:str):
    if not campo.replace(" ","").isalpha():
        return True, ERROR_CLIENTE["BAD_REQUEST"](f"El campo '{campo}' debe contener solo letras")
    return False, None

def validando_campos_registro():
    datos=request.get_json(silent=True)
    if datos is None:
        return True, ERROR_CLIENTE["UNSUPPORTED_MEDIA_TYPE"]("La request no contiene un body JSON valido")
    try:
        nombre=datos["nombre"].strip().title()
        apellido=datos["apellido"].strip().title()
        email=datos["email"]
        password=datos["password"]

        for campo in [nombre, apellido]:
            error, data = validando_solo_letras(campo)
            if error: 
                return True, data

        return False, {"nombre":nombre, "apellido":apellido, "email":email, "password":password}
    
    except Exception as e:
        if isinstance(e, KeyError):
            return True, ERROR_CLIENTE["BAD_REQUEST"](f"Falta campo obligatorio: {str(e)}")
        return True, ERROR_CLIENTE["BAD_REQUEST"](str(e))

def validar_login(body):
    error, body = validar_body_json(body)
    if error:
        return True, body
    error, email = validar_email(body)
    if error:
        return True, email
    error, password = validar_texto(body, "password", max_largo=100)
    if error:
        return True, password
    return False, {"email": email, "password": password}