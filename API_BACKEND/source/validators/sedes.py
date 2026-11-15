from flask import request
from source.utils.validaciones import validar_body_json, validar_texto

def validar_campos_sede():
    body = request.get_json(silent=True)
    error, body = validar_body_json(body)
    if error:
        return True, body
    error, nombre = validar_texto(body, "nombre", max_largo=50)
    if error:
        return True, nombre
    error, direccion = validar_texto(body, "direccion", max_largo=100)
    if error:
        return True, direccion
    return False, {"nombre": nombre, "direccion": direccion}