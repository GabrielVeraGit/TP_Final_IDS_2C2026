from functools import wraps
from flask import request
from errors_code import ERROR_CLIENTE
from source.utils import config
from source.repositories.users import obtener_usuario_por_token

def verificar_api_key():
    if not config.API_KEY:
        return None  # sin API_KEY configurada no se exige (solo para desarrollo)
    if request.headers.get("X-API-KEY", "") != config.API_KEY:
        return ERROR_CLIENTE["UNAUTHORIZED"]("API key invalida o ausente (header X-API-KEY)")
    return None

def obtener_token():
    partes = request.headers.get("Authorization", "").split(" ")
    if len(partes) != 2 or partes[0] != "Bearer" or not partes[1]:
        return True, ERROR_CLIENTE["UNAUTHORIZED"]("Falta el header Authorization: Bearer <token>")
    return False, partes[1]

def obtener_usuario_logueado():
    error, token = obtener_token()
    if error:
        return True, token
    usuario = obtener_usuario_por_token(token)
    if usuario is None:
        return True, ERROR_CLIENTE["UNAUTHORIZED"]("Sesion invalida o expirada, vuelva a iniciar sesion")
    return False, usuario


def requiere_login(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        error, resultado = obtener_usuario_logueado()
        if error:
            return resultado
        return funcion(resultado, *args, **kwargs)  
    return envoltura


def requiere_admin(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        error, resultado = obtener_usuario_logueado()
        if error:
            return resultado
        if resultado["rol"] != "admin":
            return ERROR_CLIENTE["FORBIDDEN"]("No tiene permisos para realizar esta accion")
        return funcion(*args, **kwargs)
    return envoltura
