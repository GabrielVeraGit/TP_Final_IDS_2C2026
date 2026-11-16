from errors_code import ERROR_CLIENTE



def confirmando_query_paramts(query_paramts:dict):
    qp_validas_int=("id_funcion", "id_usuario", "cant_entradas")
    
    estados_compra=('reservada', 'cancelada', 'usada')

    for qp_valida in qp_validas_int:
        dato = query_paramts.get(qp_valida, None)
        if dato is not None and dato <= 0:
            return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"{qp_valida} debe ser > 0")

    estado = query_paramts.get("estado_compra", None)
    if estado is not None and not (estado in estados_compra):
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"estado_compra solo permite: {', '.join(estados_compra)}")

    date1 = query_paramts.get("fecha_desde", None)
    date2 = query_paramts.get("fecha_hasta", None)
    if (date1 is not None) and (date2 is not None) and date1 >= date2:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("Las fechas no cumplen fecha_desde < fecha_hasta")

    return False, None
