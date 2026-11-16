from flask import request
from source.utils import validaciones as utils_val


def validando_query_paramts():
    qp_validas=("id_funcion", "id_usuario", "cant_entradas", "estado_compra",  "fecha_desde", "fecha_hasta")
    qp_func=(utils_val.validar_entero, utils_val.validar_entero, utils_val.validar_entero, utils_val.validar_texto, utils_val.validar_fecha_hora, utils_val.validar_fecha_hora)
    qp_dict = dict(zip(qp_validas, qp_func))
    qp_request = request.args
    qp_limpios = dict()

    for qp_valida in qp_validas:
        dato = qp_request.get(qp_valida, None)
        if dato is not None and dato.strip() != "":
            error, result = qp_dict[qp_valida](qp_request, qp_valida)
            if error:
                return True, result
            qp_limpios[qp_valida]=result 
    
    return False, qp_limpios

