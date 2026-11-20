from source.db import ejecutar_instruccion
from errors_code import ERROR_SERVIDOR


def obtener_ocupacion_funciones():
    query = """
        SELECT
            F.id_funcion,
            P.titulo AS pelicula,
            F.fecha_hora,
            SA.numero AS sala,
            SA.capacidad AS capacidad_total,
            CAST(COALESCE(SUM(R.cant_entradas), 0) AS SIGNED) AS entradas_ocupadas,
            SA.capacidad - CAST(COALESCE(SUM(R.cant_entradas), 0) AS SIGNED) AS entradas_disponibles,
            ROUND(
                COALESCE(SUM(R.cant_entradas), 0) * 100.0 / NULLIF(SA.capacidad, 0),
                2
            ) AS porcentaje_ocupacion
        FROM FUNCIONES F
        INNER JOIN PELICULAS P ON P.id_pelicula = F.id_pelicula
        INNER JOIN SALAS SA ON SA.id_sala = F.id_sala
        LEFT JOIN RESERVAS R
            ON R.id_funcion = F.id_funcion
            AND R.estado_compra <> 'cancelada'
        GROUP BY
            F.id_funcion, P.titulo, F.fecha_hora,
            SA.numero, SA.capacidad
        ORDER BY F.fecha_hora;
    """

    try:
        return False, ejecutar_instruccion(query)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](
            f"Error DB obtener_ocupacion_funciones: {str(e)}"
        )


def obtener_ventas_por_genero():
    query = """
        SELECT
            P.genero,
            COALESCE(SUM(R.monto_a_pagar), 0) AS total_ventas,
            COUNT(R.id_reserva) AS cantidad_reservas,
            COALESCE(SUM(R.cant_entradas), 0) AS entradas_vendidas
        FROM PELICULAS P
        INNER JOIN FUNCIONES F ON F.id_pelicula = P.id_pelicula
        LEFT JOIN RESERVAS R
            ON R.id_funcion = F.id_funcion
            AND R.estado_compra <> 'cancelada'
        GROUP BY P.genero
        ORDER BY total_ventas DESC;
    """

    try:
        return False, ejecutar_instruccion(query)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](
            f"Error DB obtener_ventas_por_genero: {str(e)}"
        )
