from errors_code import ERROR_CLIENTE
from source.repositories import salas as repo
from source.services import sedes as serv_sedes

def listar_salas(id_sede:int=None):
    if id_sede:
        error, sede = serv_sedes.obtener_sede(id_sede)
        if error:
            return True, sede
    return repo.obtener_salas(id_sede)

def obtener_sala(id_sala:int):
    error, registros = repo.obtener_sala(id_sala)
    if error:
        return True, registros
    if len(registros) == 0:
        return True, ERROR_CLIENTE["NOT_FOUND"](f"No existe la sala {id_sala}")
    return False, registros[0]


def verificar_numero_disponible(sala:dict, id_sala:int=0):
    error, registros = repo.obtener_salas_por_numero(sala["id_sede"], sala["numero"])
    if error:
        return True, registros
    for registro in registros:
        if registro["id_sala"] != id_sala:
            return True, ERROR_CLIENTE["CONFLICT"](f"La sede ya tiene una sala '{sala['numero']}'")
    return False, None


def verificar_capacidad_suficiente(id_sala:int, capacidad:int):
    error, funciones = repo.obtener_vendidas_funciones_futuras(id_sala)
    if error:
        return True, funciones
    for funcion in funciones:
        if funcion["vendidas"] > capacidad:
            return True, ERROR_CLIENTE["CONFLICT"](f"Hay funciones futuras con {funcion['vendidas']} entradas vendidas, la capacidad no puede ser menor")
    return False, None

def crear_sala(sala:dict):
    error, resultado = serv_sedes.obtener_sede(sala["id_sede"])
    if error:
        return True, resultado
    error, resultado = verificar_numero_disponible(sala)
    if error:
        return True, resultado
    return repo.append_sala(sala)

def modificar_sala(id_sala:int, sala:dict):
    error, actual = obtener_sala(id_sala)
    if error:
        return True, actual
    error, resultado = serv_sedes.obtener_sede(sala["id_sede"])
    if error:
        return True, resultado
    error, resultado = verificar_numero_disponible(sala, id_sala)
    if error:
        return True, resultado
    error, resultado = verificar_capacidad_suficiente(id_sala, sala["capacidad"])
    if error:
        return True, resultado
    return repo.actualizar_sala(id_sala, sala)

def eliminar_sala(id_sala:int):
    error, resultado = obtener_sala(id_sala)
    if error:
        return True, resultado
    error, cantidad = repo.contar_funciones_sala(id_sala)
    if error:
        return True, cantidad
    if cantidad > 0:
        return True, ERROR_CLIENTE["CONFLICT"]("La sala tiene funciones programadas, no se puede eliminar")
    return repo.eliminar_sala(id_sala)