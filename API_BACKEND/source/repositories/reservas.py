from errors_code import ERROR_CLIENTE, ERROR_SERVIDOR
from source.db import ejecutar_instruccion, ejecutar_transaccion
from datetime import datetime

#filtros: clave=la columna filtro; valor=el dato filtro
def obtener_reservas_filtros(filtros:dict=None)-> list[dict]:
    query = "SELECT * FROM RESERVAS"
    if filtros:
        filtros_c = filtros.copy()
    else:
        filtros_c = dict()
    
    condiciones = []
    valores = []

    date1 = filtros_c.pop("fecha_desde", None)
    date2 = filtros_c.pop("fecha_hasta", None)

    if date1 is not None and date2 is not None:
        condiciones.append("fecha_de_compra BETWEEN %s AND %s")
        valores.extend([date1, date2])
    elif date1 is not None:
        condiciones.append("fecha_de_compra >= %s")
        valores.append(date1)
    elif date2 is not None:
        condiciones.append("fecha_de_compra <= %s")
        valores.append(date2)

    for columna, valor in filtros_c.items():
        condiciones.append(f"{columna} = %s")
        valores.append(valor)

    if condiciones:
        union_col = " AND ".join(condiciones)
        query = f"{query} WHERE {union_col};"
    else:
        query = f"{query};"

    try:
        if valores:
            resultado = ejecutar_instruccion(query, tuple(valores))
        else:
            resultado = ejecutar_instruccion(query)
        return False, resultado
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_reservas_filtros, {str(e)}")

def obtener_funcion_relacional_salas_sede(id_funcion:int):
    query="""
    SELECT sed.id_sede, f.*, s.numero as name_sala, s.capacidad as capacidad_sala, sed.nombre as name_sede, sed.direccion as direccion_sede, 
    (
    SELECT COALESCE(SUM(r.cant_entradas),0)
    FROM RESERVAS r
    WHERE r.id_funcion=%s AND r.estado_compra != 'cancelada'
    ) as capacidad_ocupada
    FROM FUNCIONES f
    INNER JOIN SALAS s ON f.id_sala = s.id_sala
    INNER JOIN SEDES sed ON s.id_sede = sed.id_sede
    WHERE f.id_funcion = %s;"""
    try:
        registro_funcion = ejecutar_instruccion(query, (id_funcion,id_funcion))
        return False, registro_funcion
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_funcion_relacional, {str(e)}")

def insertar_reserva_con_cupo(cursor, datos:dict):
    cursor.execute("""
    SELECT f.precio_entrada, s.capacidad AS capacidad_sala
    FROM FUNCIONES f
    INNER JOIN SALAS s ON f.id_sala = s.id_sala
    WHERE f.id_funcion = %s
    FOR UPDATE;""", (datos["id_funcion"],))
    funcion = cursor.fetchall()
    if len(funcion) == 0:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"El id_funcion={datos['id_funcion']} no existe")
    funcion = funcion[0]

    cursor.execute("""
    SELECT COALESCE(SUM(cant_entradas), 0) AS ocupadas
    FROM RESERVAS
    WHERE id_funcion = %s AND estado_compra != 'cancelada';""", (datos["id_funcion"],))
    ocupadas = int(cursor.fetchall()[0]["ocupadas"])

    capacidad_disponible = int(funcion["capacidad_sala"]) - ocupadas
    if datos["cant_entradas"] > capacidad_disponible:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"cant_entradas={datos['cant_entradas']} supera la capacidad_disponible={capacidad_disponible}")

    monto_a_pagar = datos["cant_entradas"] * funcion["precio_entrada"]
    cursor.execute("""
    INSERT INTO RESERVAS (id_funcion, id_usuario, fecha_de_compra, qr, cant_entradas, monto_a_pagar)
    VALUES (%s, %s, %s, %s, %s, %s);""",
    (datos["id_funcion"], datos["id_usuario"], datetime.now(), datos["qr"], datos["cant_entradas"], monto_a_pagar))
    return False, None


def crear_reserva(body:dict, qr:str):
    datos = {"id_funcion": body["id_funcion"],
             "id_usuario": body["id_usuario"],
             "cant_entradas": body["cant_entradas"],
             "qr": qr}
    try:
        error, resultado = ejecutar_transaccion(insertar_reserva_con_cupo, datos)
        return error, resultado
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB crear_reserva, {str(e)}")



def actualizar_estado_reserva(registro: dict, qr_id: str, nuevo_estado: str, columna_fecha: str):
    query = f"""UPDATE RESERVAS SET estado_compra=%s, {columna_fecha}=%s WHERE id_reserva=%s AND qr=%s;"""
    try:
        result = ejecutar_instruccion(query, (nuevo_estado, datetime.now(), registro["id_reserva"], qr_id), autocommit=True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB actualizar_estado ({nuevo_estado}): {str(e)}")



def cancelar_reserva(registro: dict, qr_id: str):
    return actualizar_estado_reserva(registro, qr_id, "cancelada", "fecha_cancelacion")


def usar_reserva(registro: dict, qr_id: str):
    return actualizar_estado_reserva(registro, qr_id, "usada", "fecha_validacion")
