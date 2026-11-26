from flask import request
from source.utils.validaciones import validar_body_json, validar_texto, validar_entero, validar_fecha_hora, error_validacion


def validar_disponibilidad(body:dict):
    error, desde = validar_fecha_hora(body, "disponible_desde", obligatorio=False)
    if error:
        return True, desde
    error, hasta = validar_fecha_hora(body, "disponible_hasta", obligatorio=False)
    if error:
        return True, hasta
    if desde and hasta and desde >= hasta:
        return error_validacion("'disponible_desde' debe ser anterior a 'disponible_hasta'")
    return False, {"disponible_desde": desde, "disponible_hasta": hasta}

def validar_importacion():
    body = request.get_json(silent=True)
    error, body = validar_body_json(body)
    if error:
        return True, body
    error, titulo = validar_texto(body, "titulo", max_largo=100)
    if error:
        return True, titulo
    error, anio = validar_entero(body, "anio", obligatorio=False, minimo=1888, maximo=2100)
    if error:
        return True, anio
    error, disponibilidad = validar_disponibilidad(body)
    if error:
        return True, disponibilidad
    disponibilidad["titulo"] = titulo
    disponibilidad["anio"] = anio
    return False, disponibilidad

def validar_modificacion():
    body = request.get_json(silent=True)
    error, body = validar_body_json(body)
    if error:
        return True, body
    return validar_disponibilidad(body)

def validar_filtros_peliculas():
    error, titulo = validar_texto(request.args, "titulo", obligatorio=False, max_largo=100)
    if error:
        return True, titulo
    error, genero = validar_texto(request.args, "genero", obligatorio=False, max_largo=50)
    if error:
        return True, genero
    error, id_sede = validar_entero(request.args, "id_sede", obligatorio=False, minimo=1)
    if error:
        return True, id_sede
    return False, {"titulo": titulo, "genero": genero, "id_sede": id_sede}