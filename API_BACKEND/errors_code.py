from flask import jsonify, Response

def return_final(code:str, message:str, level:str, descripcion:str, code_n:int )-> tuple[Response, int]:
    lista = [{
        "code": code,
        "message": message,
        "level": level,
        "description": descripcion
    }]
    return jsonify({"errors":lista}), code_n

def bad_request(descripcion:str):
    return return_final(
        "BAD_REQUEST",
        "La request contiene sintaxis inválida, parámetros faltantes o datos mal formateados",
        "ERROR_CLIENT",
        descripcion, 
        400)

def no_autorizado(descripcion:str):
    return return_final(
        "UNAUTHORIZED",
        "Requiere autenticacion, la request carece de credenciales válidas (tokens, cookies de sesión o encabezados de autorización)",
        "ERROR_CLIENT",
        descripcion,
        401)

def prohibido(descripcion:str):
    return return_final(
        "FORBIDDEN",
        "Cliente está autenticado, pero no tiene los permisos suficientes para acceder al recurso solicitado",
        "ERROR_CLIENT",
        descripcion,
        403)

def not_found(descripcion:str):
    return return_final(
        "NOT_FOUND",
        "El recurso o la ruta URL no existe",
        "ERROR_CLIENT",
        descripcion,
        404)

def metodo_no_permitido(descripcion:str):
    return return_final(
        "METHOD_NOT_ALLOWED",
        "La ruta existe, pero no admite el método HTTP utilizado",
        "ERROR_CLIENT",
        descripcion,
        405)

def conflicto(descripcion:str):
    return return_final(
        "CONFLICT",
        "La solicitud entra en conflicto con el estado actual del recurso en la db",
        "ERROR_CLIENT",
        descripcion,
        409)

def formato_no_soportado(descripcion:str):
    return return_final(
        "UNSUPPORTED_MEDIA_TYPE",
        "El formato del contenido enviado no está soportado",
        "ERROR_CLIENT",
        descripcion,
        415)

def entidad_no_procesable(descripcion:str):
    return return_final(
        "UNPROCESSABLE_ENTITY",
        "Datos y formato correctos, pero no cumplen con las reglas de negocio",
        "ERROR_CLIENT",
        descripcion,
        422)

def error_interno(descripcion:str):
    return return_final(
        "INTERNAL_SERVER_ERROR",
        "Error interno del servidor",
        "ERROR_SERVER",
        descripcion,
        500)

ERROR_CLIENTE={
    "BAD_REQUEST": bad_request,
    "UNAUTHORIZED": no_autorizado,
    "FORBIDDEN": prohibido,
    "NOT_FOUND": not_found,
    "METHOD_NOT_ALLOWED": metodo_no_permitido,
    "CONFLICT": conflicto,
    "UNSUPPORTED_MEDIA_TYPE": formato_no_soportado,
    "UNPROCESSABLE_ENTITY": entidad_no_procesable
}

ERROR_SERVIDOR = {
    "INTERNAL_SERVER_ERROR": error_interno
}

#ejemplo: return ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("El campo 'nombre' es obligatorio y no puede estar vacío.")
