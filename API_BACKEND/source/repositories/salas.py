from source.db import ejecutar_instruccion, ejecutar_insercion
from errors_code import ERROR_SERVIDOR


def obtener_salas(id_sede:int=None):
    query = """SELECT S.id_sala, S.id_sede, SE.nombre AS sede, S.numero, S.capacidad
               FROM SALAS S
               JOIN SEDES SE ON SE.id_sede = S.id_sede"""
    valores = ()
    if id_sede:
        query = f"{query} WHERE S.id_sede = %s"
        valores = (id_sede,)
    query = f"{query} ORDER BY SE.nombre, S.numero;"
    try:
        return False, ejecutar_instruccion(query, valores)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_salas, {str(e)}")

def obtener_sala(id_sala:int):
    query = """SELECT S.id_sala, S.id_sede, SE.nombre AS sede, S.numero, S.capacidad
               FROM SALAS S
               JOIN SEDES SE ON SE.id_sede = S.id_sede
               WHERE S.id_sala = %s;"""
    try:
        return False, ejecutar_instruccion(query, (id_sala,))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_sala, {str(e)}")


def obtener_salas_por_numero(id_sede:int, numero:str):
    query = "SELECT id_sala FROM SALAS WHERE id_sede = %s AND numero = %s;"
    try:
        return False, ejecutar_instruccion(query, (id_sede, numero))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_salas_por_numero, {str(e)}")


def append_sala(sala:dict):
    query = "INSERT INTO SALAS (id_sede, numero, capacidad) VALUES (%s, %s, %s);"
    try:
        id_sala = ejecutar_insercion(query, (sala["id_sede"], sala["numero"], sala["capacidad"]))
        return False, id_sala
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB append_sala, {str(e)}")

def actualizar_sala(id_sala:int, sala:dict):
    query = "UPDATE SALAS SET id_sede = %s, numero = %s, capacidad = %s WHERE id_sala = %s;"
    try:
        ejecutar_instruccion(query, (sala["id_sede"], sala["numero"], sala["capacidad"], id_sala), True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB actualizar_sala, {str(e)}")

def eliminar_sala(id_sala:int):
    query = "DELETE FROM SALAS WHERE id_sala = %s;"
    try:
        ejecutar_instruccion(query, (id_sala,), True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB eliminar_sala, {str(e)}")

def contar_funciones_sala(id_sala:int):
    query = "SELECT COUNT(*) AS cantidad FROM FUNCIONES WHERE id_sala = %s;"
    try:
        return False, ejecutar_instruccion(query, (id_sala,))[0]["cantidad"]
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB contar_funciones_sala, {str(e)}")


def obtener_vendidas_funciones_futuras(id_sala:int):
    query = """SELECT CAST(SUM(R.cant_entradas) AS SIGNED) AS vendidas
               FROM RESERVAS R
               JOIN FUNCIONES F ON F.id_funcion = R.id_funcion
               WHERE F.id_sala = %s AND F.fecha_hora > NOW() AND R.estado_compra <> 'cancelada'
               GROUP BY F.id_funcion;"""
    try:
        return False, ejecutar_instruccion(query, (id_sala,))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_vendidas_funciones_futuras, {str(e)}")