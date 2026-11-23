from functools import wraps
from flask import request
from errors_code import ERROR_CLIENTE
from source.utils import config


def verificar_api_key():
    if not config.API_KEY:
        return None  # sin API_KEY configurada no se exige (solo para desarrollo)
    if request.headers.get("X-API-KEY", "") != config.API_KEY:
        return ERROR_CLIENTE["UNAUTHORIZED"]("API key invalida o ausente (header X-API-KEY)")
    return None


