from flask import request
from source.utils.validaciones import validar_body_json, validar_entero, validar_decimal, validar_fecha_hora, validar_rango_fechas, validar_ids_opcionales

def validar_campos_funcion():
    body = request.get_json(silent=True)
    error, body = validar_body_json(body)
    if error:
        return True, body
    error, id_pelicula = validar_entero(body, "id_pelicula", minimo=1)
    if error:
        return True, id_pelicula
    error, id_sala = validar_entero(body, "id_sala", minimo=1)
    if error:
        return True, id_sala
    error, fecha_hora = validar_fecha_hora(body, "fecha_hora")
    if error:
        return True, fecha_hora
    error, precio = validar_decimal(body, "precio_entrada", minimo=1)
    if error:
        return True, precio
    return False, {"id_pelicula": id_pelicula, "id_sala": id_sala, "fecha_hora": fecha_hora, "precio_entrada": precio}

#Filtros opcionales de la query string: id_pelicula, id_sede, id_sala, desde, hasta
def validar_filtros_funciones():
    error, filtros = validar_ids_opcionales(request.args, ("id_pelicula", "id_sede", "id_sala"))
    if error:
        return True, filtros
    error, fechas = validar_rango_fechas(request.args)
    if error:
        return True, fechas
    filtros["desde"] = fechas["desde"]
    filtros["hasta"] = fechas["hasta"]
    return False, filtros