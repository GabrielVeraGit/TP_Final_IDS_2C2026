from datetime import datetime, timedelta
from errors_code import ERROR_CLIENTE
from source.utils import config
from source.repositories import funciones as repo
from source.services import peliculas as serv_peliculas
from source.services import salas as serv_salas

#Sin "desde" solo muestra las funciones que todavia no empezaron
def listar_funciones(filtros:dict):
    if filtros["desde"] is None:
        filtros["desde"] = datetime.now()
    return repo.obtener_funciones(filtros)

def obtener_funcion(id_funcion:int):
    error, registros = repo.obtener_funciones({"id_funcion": id_funcion})
    if error:
        return True, registros
    if len(registros) == 0:
        return True, ERROR_CLIENTE["NOT_FOUND"](f"No existe la funcion {id_funcion}")
    return False, registros[0]

#Si la pelicula no tiene duracion se usa la de por defecto
def obtener_duracion_minutos(duracion:str):
    partes = str(duracion).split(" ")
    if partes[0].isdigit():
        return int(partes[0])
    return config.DURACION_POR_DEFECTO_MIN

def verificar_disponibilidad_pelicula(pelicula:dict, fecha_hora:datetime):
    desde = pelicula["disponible_desde"]
    hasta = pelicula["disponible_hasta"]
    if desde and fecha_hora < desde:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"La pelicula esta disponible desde {desde}")
    if hasta and fecha_hora > hasta:
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"La pelicula esta disponible hasta {hasta}")
    return False, None

#Dos funciones de una sala no pueden superponerse y entre ambas deben pasar los minutos de limpieza
def verificar_sala_libre(datos:dict, pelicula:dict, id_funcion:int=0):
    limpieza = timedelta(minutes=config.MINUTOS_ENTRE_FUNCIONES)
    inicio = datos["fecha_hora"]
    fin = inicio + timedelta(minutes=obtener_duracion_minutos(pelicula["duracion"]))

    error, otras = repo.obtener_funciones_sala_entre(datos["id_sala"], inicio - timedelta(days=1), fin + timedelta(days=1))
    if error:
        return True, otras
    for otra in otras:
        if otra["id_funcion"] == id_funcion:
            continue
        inicio_otra = otra["fecha_hora"]
        fin_otra = inicio_otra + timedelta(minutes=obtener_duracion_minutos(otra["duracion"]))
        if inicio < fin_otra + limpieza and inicio_otra < fin + limpieza:
            return True, ERROR_CLIENTE["CONFLICT"](f"La sala esta ocupada por la funcion {otra['id_funcion']} ({inicio_otra} a {fin_otra}), se necesitan {config.MINUTOS_ENTRE_FUNCIONES} min entre funciones")
    return False, None

def verificar_reglas_funcion(datos:dict, id_funcion:int=0):
    error, pelicula = serv_peliculas.obtener_pelicula(datos["id_pelicula"])
    if error:
        return True, pelicula
    error, sala = serv_salas.obtener_sala(datos["id_sala"])
    if error:
        return True, sala
    if datos["fecha_hora"] <= datetime.now():
        return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"]("La funcion debe programarse en una fecha futura")
    error, resultado = verificar_disponibilidad_pelicula(pelicula, datos["fecha_hora"])
    if error:
        return True, resultado
    return verificar_sala_libre(datos, pelicula, id_funcion)

def crear_funcion(datos:dict):
    error, resultado = verificar_reglas_funcion(datos)
    if error:
        return True, resultado
    return repo.append_funcion(datos)


def verificar_cambios_permitidos(actual:dict, datos:dict):
    if actual["fecha_hora"] <= datetime.now():
        return True, ERROR_CLIENTE["CONFLICT"]("La funcion ya comenzo, no se puede modificar")
    if actual["entradas_vendidas"] == 0:
        return False, None
    if datos["id_pelicula"] != actual["id_pelicula"] or datos["id_sala"] != actual["id_sala"] or datos["fecha_hora"] != actual["fecha_hora"]:
        return True, ERROR_CLIENTE["CONFLICT"]("La funcion tiene entradas vendidas, solo se puede modificar el precio")
    return False, None

def modificar_funcion(id_funcion:int, datos:dict):
    error, actual = obtener_funcion(id_funcion)
    if error:
        return True, actual
    error, resultado = verificar_cambios_permitidos(actual, datos)
    if error:
        return True, resultado
    error, resultado = verificar_reglas_funcion(datos, id_funcion)
    if error:
        return True, resultado
    return repo.actualizar_funcion(id_funcion, datos)

def eliminar_funcion(id_funcion:int):
    error, actual = obtener_funcion(id_funcion)
    if error:
        return True, actual
    if actual["entradas_vendidas"] > 0:
        return True, ERROR_CLIENTE["CONFLICT"]("La funcion tiene entradas vendidas, no se puede eliminar")
    return repo.eliminar_funcion(id_funcion)