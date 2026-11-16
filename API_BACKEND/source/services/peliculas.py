import requests
from errors_code import ERROR_CLIENTE, ERROR_SERVIDOR
from source.utils import config
from source.repositories import peliculas as repo

def listar_peliculas(filtros:dict, solo_cartelera:bool=False):
    return repo.obtener_peliculas(filtros, solo_cartelera)

def obtener_pelicula(id_pelicula:int):
    error, registros = repo.obtener_pelicula(id_pelicula)
    if error:
        return True, registros
    if len(registros) == 0:
        return True, ERROR_CLIENTE["NOT_FOUND"](f"No existe la pelicula {id_pelicula}")
    return False, registros[0]

def consultar_omdb(titulo:str, anio:int=None):
    parametros = {"apikey": config.OMDB_API_KEY, "t": titulo}
    if anio:
        parametros["y"] = anio
    try:
        respuesta = requests.get(config.OMDB_URL, params=parametros, timeout=config.TIMEOUT_OMDB_SEG)
        datos = respuesta.json()
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"No se pudo consultar OMDb, motivo: {str(e)}")
    if datos.get("Response") != "True":
        return True, ERROR_CLIENTE["NOT_FOUND"](f"OMDb: {datos.get('Error', 'pelicula no encontrada')}")
    return False, datos

def convertir_formato_omdb(datos:dict, disponibilidad:dict):
    return {
        "titulo": datos["Title"],
        "anio": int(datos["Year"][:4]),#a veces viene "2019-" (series)
        "clasificacion": datos.get("Rated"),
        "duracion": datos.get("Runtime"),
        "genero": datos.get("Genre"),
        "director": datos.get("Director"),
        "actores": datos.get("Actors"),
        "sinopsis": datos.get("Plot"),
        "lenguaje": datos.get("Language"),
        "poster": datos.get("Poster"),
        "omdb_id": datos["imdbID"],
        "disponible_desde": disponibilidad["disponible_desde"],
        "disponible_hasta": disponibilidad["disponible_hasta"]
    }

def importar_pelicula(datos:dict):
    error, resultado = consultar_omdb(datos["titulo"], datos["anio"])
    if error:
        return True, resultado
    pelicula = convertir_formato_omdb(resultado, datos)

    error, existentes = repo.obtener_pelicula_por_omdb(pelicula["omdb_id"])
    if error:
        return True, existentes
    if len(existentes) > 0:
        return True, ERROR_CLIENTE["CONFLICT"](f"La pelicula '{pelicula['titulo']}' ya fue importada")
    return repo.append_pelicula(pelicula)

def verificar_funciones_en_rango(id_pelicula:int, disponibilidad:dict):
    error, funciones = repo.obtener_fechas_funciones_futuras(id_pelicula)
    if error:
        return True, funciones
    for funcion in funciones:
        fecha = funcion["fecha_hora"]
        if disponibilidad["disponible_desde"] and fecha < disponibilidad["disponible_desde"]:
            return True, ERROR_CLIENTE["CONFLICT"](f"Hay una funcion el {fecha} anterior al nuevo 'disponible_desde'")
        if disponibilidad["disponible_hasta"] and fecha > disponibilidad["disponible_hasta"]:
            return True, ERROR_CLIENTE["CONFLICT"](f"Hay una funcion el {fecha} posterior al nuevo 'disponible_hasta'")
    return False, None

def modificar_disponibilidad(id_pelicula:int, disponibilidad:dict):
    error, resultado = obtener_pelicula(id_pelicula)
    if error:
        return True, resultado
    error, resultado = verificar_funciones_en_rango(id_pelicula, disponibilidad)
    if error:
        return True, resultado
    return repo.actualizar_disponibilidad(id_pelicula, disponibilidad)

def eliminar_pelicula(id_pelicula:int):
    error, resultado = obtener_pelicula(id_pelicula)
    if error:
        return True, resultado
    error, cantidad = repo.contar_funciones_pelicula(id_pelicula)
    if error:
        return True, cantidad
    if cantidad > 0:
        return True, ERROR_CLIENTE["CONFLICT"]("La pelicula tiene funciones programadas, no se puede eliminar (modifique su disponibilidad para sacarla de cartelera)")
    return repo.eliminar_pelicula(id_pelicula)