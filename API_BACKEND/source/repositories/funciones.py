from source.db import ejecutar_instruccion, ejecutar_insercion
from errors_code import ERROR_SERVIDOR
from source.repositories import reservas as repo_reservas


def armar_where_funciones(filtros:dict):
    condiciones_posibles = {
        "id_funcion": "F.id_funcion = %s",
        "id_pelicula": "F.id_pelicula = %s",
        "id_sede": "SA.id_sede = %s",
        "id_sala": "F.id_sala = %s",
        "desde": "F.fecha_hora >= %s",
        "hasta": "F.fecha_hora <= %s"
    }
    condiciones = []
    valores = []
    for filtro, condicion in condiciones_posibles.items():
        if filtros.get(filtro):
            condiciones.append(condicion)
            valores.append(filtros[filtro])
    if len(condiciones) == 0:
        return "", ()
    return " WHERE " + " AND ".join(condiciones), tuple(valores)


def obtener_funciones(filtros:dict):
    error, resultado = repo_reservas.vencer_pagos_pendientes()
    if error:
        return True, resultado
    where, valores = armar_where_funciones(filtros)
    query = f"""SELECT F.id_funcion, F.fecha_hora, F.precio_entrada,
                       P.id_pelicula, P.titulo, P.poster, P.duracion,
                       SE.id_sede, SE.nombre AS sede, SA.id_sala, SA.numero AS sala, SA.capacidad,
                       CAST(COALESCE(SUM(R.cant_entradas), 0) AS SIGNED) AS entradas_vendidas,
                       SA.capacidad - CAST(COALESCE(SUM(R.cant_entradas), 0) AS SIGNED) AS entradas_disponibles
                FROM FUNCIONES F
                JOIN PELICULAS P ON P.id_pelicula = F.id_pelicula
                JOIN SALAS SA ON SA.id_sala = F.id_sala
                JOIN SEDES SE ON SE.id_sede = SA.id_sede
                LEFT JOIN RESERVAS R ON R.id_funcion = F.id_funcion AND R.estado_compra <> 'cancelada'
                {where}
                GROUP BY F.id_funcion, F.fecha_hora, F.precio_entrada, P.id_pelicula, P.titulo, P.poster, P.duracion,
                         SE.id_sede, SE.nombre, SA.id_sala, SA.numero, SA.capacidad
                ORDER BY F.fecha_hora;"""
    try:
        return False, ejecutar_instruccion(query, valores)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_funciones, {str(e)}")


def obtener_funciones_sala_entre(id_sala:int, desde, hasta):
    query = """SELECT F.id_funcion, F.fecha_hora, P.duracion
               FROM FUNCIONES F
               JOIN PELICULAS P ON P.id_pelicula = F.id_pelicula
               WHERE F.id_sala = %s AND F.fecha_hora BETWEEN %s AND %s;"""
    try:
        return False, ejecutar_instruccion(query, (id_sala, desde, hasta))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_funciones_sala_entre, {str(e)}")


def append_funcion(funcion:dict):
    query = "INSERT INTO FUNCIONES (id_pelicula, id_sala, fecha_hora, precio_entrada) VALUES (%s, %s, %s, %s);"
    valores = (funcion["id_pelicula"], funcion["id_sala"], funcion["fecha_hora"], funcion["precio_entrada"])
    try:
        return False, ejecutar_insercion(query, valores)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB append_funcion, {str(e)}")

def actualizar_funcion(id_funcion:int, funcion:dict):
    query = "UPDATE FUNCIONES SET id_pelicula = %s, id_sala = %s, fecha_hora = %s, precio_entrada = %s WHERE id_funcion = %s;"
    valores = (funcion["id_pelicula"], funcion["id_sala"], funcion["fecha_hora"], funcion["precio_entrada"], id_funcion)
    try:
        ejecutar_instruccion(query, valores, True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB actualizar_funcion, {str(e)}")

def eliminar_funcion(id_funcion:int):
    query = "DELETE FROM FUNCIONES WHERE id_funcion = %s;"
    try:
        ejecutar_instruccion(query, (id_funcion,), True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB eliminar_funcion, {str(e)}")