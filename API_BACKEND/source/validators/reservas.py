from flask import request
from source.utils import validaciones as utils_val
from errors_code import ERROR_CLIENTE


#valida los campos, y los retorna casteados
def validando_campos_reserva(datos_revisar:dict):
    datos_str = dict()
    for clave, valor in datos_revisar.items():
        if valor is not None:
            datos_str[clave] = str(valor)
    
    campos_relacion = {
    "id_reserva": utils_val.validar_entero,
    "id_funcion": utils_val.validar_entero,
    "id_usuario": utils_val.validar_entero,
    "cant_entradas": utils_val.validar_entero,
    "estado_compra": utils_val.validar_texto,
    "fecha_desde": utils_val.validar_fecha_hora,
    "fecha_hasta": utils_val.validar_fecha_hora,
    "qr": utils_val.validar_texto
    }

    campos_limpios = dict()

    for campo, func in campos_relacion.items():
        dato_r = datos_str.get(campo, None)
        if (dato_r is not None) and (dato_r.strip() != ""):
            error, result = func(datos_str, campo)
            if error:
                return True, result
            
            campos_limpios[campo] = result 
    
    return False, campos_limpios

def validando_query_paramts():
    error, result = validando_campos_reserva(request.args)
    if error:
        return True, result
    return False, result

def validando_json():
    body = request.get_json(silent=True)
    error, result = utils_val.validar_body_json(body)
    if error:
        return True, result
    try:
        id_f=body["id_funcion"]
        cant_entradas=body["cant_entradas"]
    except KeyError as e:
        return True, ERROR_CLIENTE["BAD_REQUEST"](f"Datos faltantes, {str(e)}")
    
    error, result = validando_campos_reserva(body)
    if error:
        return True, result
    return False, result