from flask import request
from source.utils.validaciones import validar_body_json, validar_texto, validar_entero, validar_ids_opcionales

def validar_campos_sala():
    body = request.get_json(silent=True)
    error, body = validar_body_json(body)
    if error:
        return True, body
    error, id_sede = validar_entero(body, "id_sede", minimo=1)
    if error:
        return True, id_sede
    error, numero = validar_texto(body, "numero", max_largo=50)
    if error:
        return True, numero
    error, capacidad = validar_entero(body, "capacidad", minimo=1, maximo=1000)
    if error:
        return True, capacidad
    return False, {"id_sede": id_sede, "numero": numero, "capacidad": capacidad}

def validar_filtros_salas():
    return validar_ids_opcionales(request.args, ("id_sede",))