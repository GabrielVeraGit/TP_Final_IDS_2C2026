import re
from datetime import datetime
from errors_code import ERROR_CLIENTE

FORMATOS_FECHA_HORA = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d")
PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def error_validacion(mensaje: str):
    return True, ERROR_CLIENTE["BAD_REQUEST"](mensaje)


def validar_body_json(body):
    if not isinstance(body, dict):
        return True, ERROR_CLIENTE["UNSUPPORTED_MEDIA_TYPE"]("La request no contiene un body JSON valido")
    return False, body


def esta_vacio(valor) -> bool:
    return valor is None or (isinstance(valor, str) and valor.strip() == "")


def validar_texto(datos: dict, campo: str, obligatorio: bool = True, max_largo: int = 255):
    valor = datos.get(campo)
    if esta_vacio(valor):
        if obligatorio:
            return error_validacion(f"El campo '{campo}' es obligatorio")
        return False, None
    if not isinstance(valor, str):
        return error_validacion(f"El campo '{campo}' debe ser texto")
    valor = valor.strip()
    if len(valor) > max_largo:
        return error_validacion(f"El campo '{campo}' no puede superar los {max_largo} caracteres")
    return False, valor


def validar_entero(datos: dict, campo: str, obligatorio: bool = True, minimo: int = None, maximo: int = None):
    valor = datos.get(campo)
    if esta_vacio(valor):
        if obligatorio:
            return error_validacion(f"El campo '{campo}' es obligatorio")
        return False, None
    if isinstance(valor, bool) or isinstance(valor, float):
        return error_validacion(f"El campo '{campo}' debe ser un numero entero")
    try:
        numero = int(valor)
    except (ValueError, TypeError):
        return error_validacion(f"El campo '{campo}' debe ser un numero entero")
    if minimo is not None and numero < minimo:
        return error_validacion(f"El campo '{campo}' debe ser mayor o igual a {minimo}")
    if maximo is not None and numero > maximo:
        return error_validacion(f"El campo '{campo}' debe ser menor o igual a {maximo}")
    return False, numero


def validar_decimal(datos: dict, campo: str, minimo: float = 0, maximo: float = None):
    valor = datos.get(campo)
    if esta_vacio(valor):
        return error_validacion(f"El campo '{campo}' es obligatorio")
    if isinstance(valor, bool):
        return error_validacion(f"El campo '{campo}' debe ser un numero")
    try:
        numero = round(float(valor), 2)
    except (ValueError, TypeError):
        return error_validacion(f"El campo '{campo}' debe ser un numero")
    if numero < minimo:
        return error_validacion(f"El campo '{campo}' debe ser mayor o igual a {minimo}")
    if maximo is not None and numero > maximo:
        return error_validacion(f"El campo '{campo}' no puede superar {maximo}")
    return False, numero


def convertir_fecha_hora(valor: str):
    for formato in FORMATOS_FECHA_HORA:
        try:
            return datetime.strptime(valor.strip(), formato)
        except ValueError:
            pass
    return None


def validar_fecha_hora(datos: dict, campo: str, obligatorio: bool = True):
    valor = datos.get(campo)
    if esta_vacio(valor):
        if obligatorio:
            return error_validacion(f"El campo '{campo}' es obligatorio")
        return False, None
    fecha = None
    if isinstance(valor, str):
        fecha = convertir_fecha_hora(valor)
    if fecha is None:
        return error_validacion(f"El campo '{campo}' debe tener formato 'YYYY-MM-DD HH:MM'")
    return False, fecha


def validar_opcion(datos: dict, campo: str, opciones: tuple, obligatorio: bool = True):
    error, valor = validar_texto(datos, campo, obligatorio)
    if error:
        return True, valor
    if valor is not None and valor not in opciones:
        return error_validacion(f"El campo '{campo}' debe ser uno de: {', '.join(opciones)}")
    return False, valor


def validar_email(datos: dict, campo: str = "email"):
    error, email = validar_texto(datos, campo, max_largo=50)
    if error:
        return True, email
    if not PATRON_EMAIL.match(email):
        return error_validacion(f"El campo '{campo}' no es un email valido")
    return False, email.lower()


# Valida un rango de fechas opcional de la query string 
# Si "hasta" es solo una fecha (YYYY-MM-DD) se incluye el dia completo
def validar_rango_fechas(args):
    error, desde = validar_fecha_hora(args, "desde", obligatorio=False)
    if error:
        return True, desde
    error, hasta = validar_fecha_hora(args, "hasta", obligatorio=False)
    if error:
        return True, hasta
    if hasta and len(args.get("hasta", "").strip()) == len("YYYY-MM-DD"):
        hasta = hasta.replace(hour=23, minute=59, second=59)
    if desde and hasta and desde > hasta:
        return error_validacion("'desde' debe ser anterior a 'hasta'")
    return False, {"desde": desde, "hasta": hasta}


# Valida parametros enteros opcionales de la query string 
def validar_ids_opcionales(args, campos: tuple):
    filtros = {}
    for campo in campos:
        error, valor = validar_entero(args, campo, obligatorio=False, minimo=1)
        if error:
            return True, valor
        filtros[campo] = valor
    return False, filtros