from source.db import ejecutar_instruccion, ejecutar_insercion
from errors_code import ERROR_SERVIDOR


def obtener_peliculas(filtros:dict, solo_cartelera:bool=False):
    query = "SELECT DISTINCT P.* FROM PELICULAS P"
    condiciones = []
    valores = []
    if solo_cartelera:
        query = f"{query} JOIN FUNCIONES F ON F.id_pelicula = P.id_pelicula"
        condiciones.append("F.fecha_hora > NOW()")
        condiciones.append("(P.disponible_desde IS NULL OR P.disponible_desde <= NOW())")
        condiciones.append("(P.disponible_hasta IS NULL OR P.disponible_hasta >= NOW())")
    if filtros["titulo"]:
        condiciones.append("P.titulo LIKE %s")
        valores.append(f"%{filtros['titulo']}%")
    if filtros["genero"]:
        condiciones.append("P.genero LIKE %s")
        valores.append(f"%{filtros['genero']}%")
    if len(condiciones) > 0:
        query = f"{query} WHERE {' AND '.join(condiciones)}"
    query = f"{query} ORDER BY P.titulo;"
    try:
        return False, ejecutar_instruccion(query, tuple(valores))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_peliculas, {str(e)}")

def obtener_pelicula(id_pelicula:int):
    query = "SELECT * FROM PELICULAS WHERE id_pelicula = %s;"
    try:
        return False, ejecutar_instruccion(query, (id_pelicula,))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_pelicula, {str(e)}")

def obtener_pelicula_por_omdb(omdb_id:str):
    query = "SELECT id_pelicula FROM PELICULAS WHERE omdb_id = %s;"
    try:
        return False, ejecutar_instruccion(query, (omdb_id,))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_pelicula_por_omdb, {str(e)}")


def append_pelicula(pelicula:dict):
    query = """INSERT INTO PELICULAS (titulo, anio, clasificacion, duracion, genero, director, actores,
                                      sinopsis, lenguaje, poster, omdb_id, disponible_desde, disponible_hasta)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    valores = (pelicula["titulo"], pelicula["anio"], pelicula["clasificacion"], pelicula["duracion"],
               pelicula["genero"], pelicula["director"], pelicula["actores"], pelicula["sinopsis"],
               pelicula["lenguaje"], pelicula["poster"], pelicula["omdb_id"],
               pelicula["disponible_desde"], pelicula["disponible_hasta"])
    try:
        return False, ejecutar_insercion(query, valores)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB append_pelicula, {str(e)}")

def actualizar_disponibilidad(id_pelicula:int, disponibilidad:dict):
    query = "UPDATE PELICULAS SET disponible_desde = %s, disponible_hasta = %s WHERE id_pelicula = %s;"
    valores = (disponibilidad["disponible_desde"], disponibilidad["disponible_hasta"], id_pelicula)
    try:
        ejecutar_instruccion(query, valores, True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB actualizar_disponibilidad, {str(e)}")

def eliminar_pelicula(id_pelicula:int):
    query = "DELETE FROM PELICULAS WHERE id_pelicula = %s;"
    try:
        ejecutar_instruccion(query, (id_pelicula,), True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB eliminar_pelicula, {str(e)}")

def contar_funciones_pelicula(id_pelicula:int):
    query = "SELECT COUNT(*) AS cantidad FROM FUNCIONES WHERE id_pelicula = %s;"
    try:
        return False, ejecutar_instruccion(query, (id_pelicula,))[0]["cantidad"]
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB contar_funciones_pelicula, {str(e)}")

def obtener_fechas_funciones_futuras(id_pelicula:int):
    query = "SELECT fecha_hora FROM FUNCIONES WHERE id_pelicula = %s AND fecha_hora > NOW();"
    try:
        return False, ejecutar_instruccion(query, (id_pelicula,))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_fechas_funciones_futuras, {str(e)}")