from errors_code import ERROR_CLIENTE
from source.repositories import reservas as repo
from source import extend_jwt
from source.utils import config
from datetime import datetime, timedelta

def confirmando_campos(campos:dict):
    campos_validos_int=("id_funcion", "id_usuario", "cant_entradas")
    
    estados_compra=('reservada', 'cancelada', 'usada')

    for campo in campos_validos_int:
        dato = campos.get(campo, None)
        if dato is not None and dato <= 0:
            return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"{campo} debe ser > 0")

    estado = campos.get("estado_compra", None)
    if estado is not None and not (estado in estados_compra):
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"estado_compra solo permite: {', '.join(estados_compra)}")

    date1 = campos.get("fecha_desde", None)
    date2 = campos.get("fecha_hasta", None)
    if (date1 is not None) and (date2 is not None) and date1 >= date2:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("Las fechas no cumplen fecha_desde < fecha_hasta")

    return False, None

def confirmando_query_paramts(query_paramts:dict):
    error, result = confirmando_campos(query_paramts)
    if error:
        return True, result
    
    return False, None

def confirmando_json(json:dict):
    error, result = confirmando_campos(json)
    if error:
        return True, result
    return False, None

#empezemos la logica de negocio como tal
def confirmando_reserva(body:dict):
    error, registro = repo.obtener_funcion_relacional_salas_sede(body["id_funcion"])
    if error:
        return True, registro
    elif len(registro) == 0:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"El id_funcion={body['id_funcion']} no existe")
    
    registro = registro[0]

    if datetime.now() >= registro["fecha_hora"]:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"La funcion ya comenzo o termino")

    if body["cant_entradas"] > config.MAX_ENTRADAS_POR_RESERVA:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"Maximo {config.MAX_ENTRADAS_POR_RESERVA} entradas por reserva")
    
    return False, registro

def buscar_reserva_del_cliente(qr_id:str):
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, registro_re = repo.obtener_reservas_filtros({"id_usuario":data_extra["id_usuario"],"qr":qr_id})
    if error:
        return True, registro_re

    if len(registro_re) == 0:
        return True, ERROR_CLIENTE["BAD_REQUEST"]("qr_id y el cliente no coinciden")
    return False, registro_re[0]


def confirmando_pendiente_de_pago(qr_id:str):
    error, registro_re = buscar_reserva_del_cliente(qr_id)
    if error:
        return True, registro_re

    if registro_re["estado_pago"] == "vencida":
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"El tiempo para pagar ({config.MINUTOS_LIMITE_PAGO} minutos) vencio, hace una nueva reserva")
    if registro_re["estado_compra"] != "reservada":
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"La reserva esta {registro_re['estado_compra']}, no es posible pagarla")
    if registro_re["estado_pago"] == "pagada":
        return True, ERROR_CLIENTE["CONFLICT"]("La reserva ya fue pagada")
    return False, registro_re


def calcular_segundos_restantes(registro_re:dict):
    vence = registro_re["fecha_de_compra"] + timedelta(minutes=config.MINUTOS_LIMITE_PAGO)
    segundos = int((vence - datetime.now()).total_seconds())
    if segundos < 0:
        return 0
    return segundos


def confirmando_pago(qr_id:str):
    error, registro_re = confirmando_pendiente_de_pago(qr_id)
    if error:
        return True, registro_re

    error, registro_fun = repo.obtener_funcion_relacional_salas_sede(registro_re["id_funcion"])
    if error:
        return True, registro_fun
    registro_fun = registro_fun[0]

    if datetime.now() >= registro_fun["fecha_hora"]:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("La funcion ya comenzo, no es posible pagar la reserva")

    registro_fun["id_reserva"] = registro_re["id_reserva"]
    registro_fun["cant_entradas"] = registro_re["cant_entradas"]
    registro_fun["monto_a_pagar"] = registro_re["monto_a_pagar"]
    return False, registro_fun


def confirmando_cancelacion(qr_id:str):
    error, registro_re = buscar_reserva_del_cliente(qr_id)
    if error:
        return True, registro_re

    if registro_re["estado_compra"] != "reservada":
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"La reserva esta {registro_re['estado_compra']}, no es posible cancelarlo")
    
    error, registro_fun = repo.obtener_funcion_relacional_salas_sede(registro_re["id_funcion"])
    if error:
        return True, registro_fun

    registro_fun=registro_fun[0]

    hora_limite_cancelar=registro_fun["fecha_hora"] - timedelta(hours=config.HORAS_LIMITE_CANCELACION)

    if datetime.now() >= hora_limite_cancelar:
            return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"Ya no es posible cancelar la reserva, supero el tiempo limite")

    return False, registro_re
    
    
def confirmando_uso(qr_id:str):

    error, registro_re = repo.obtener_reservas_filtros({"qr":qr_id})
    if error:
        return True, registro_re
    
    if len(registro_re) == 0:
        return True, ERROR_CLIENTE["BAD_REQUEST"]("qr_id no existe")
    registro_re=registro_re[0]

    if registro_re["estado_compra"] != "reservada":
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"La reserva esta {registro_re['estado_compra']}, no es posible usarla")
    if registro_re["estado_pago"] != "pagada":
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("La reserva todavia no fue pagada")

    
    error, registro_fun = repo.obtener_funcion_relacional_salas_sede(registro_re["id_funcion"])
    if error:
        return True, registro_fun

    registro_fun=registro_fun[0]

    hora_inicial_usar=registro_fun["fecha_hora"] - timedelta(minutes=config.MINUTOS_ANTES_VALIDACION_QR)
    hora_final_usar=registro_fun["fecha_hora"] + timedelta(minutes=config.MINUTOS_DESPUES_VALIDACION_QR)

    ahora = datetime.now()
    if ahora < hora_inicial_usar:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("No es posible usar la reserva, no llego la hora de escanear")
    if ahora > hora_final_usar:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("No es posible usar la reserva, el tiempo para escanear ya paso")

    return False, registro_re