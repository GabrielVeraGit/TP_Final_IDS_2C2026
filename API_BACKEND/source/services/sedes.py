from errors_code import ERROR_CLIENTE
from source.repositories import sedes as repo

def listar_sedes():
    return repo.obtener_sedes()

def obtener_sede(id_sede:int):
    error, registros = repo.obtener_sede(id_sede)
    if error:
        return True, registros
    if len(registros) == 0:
        return True, ERROR_CLIENTE["NOT_FOUND"](f"No existe la sede {id_sede}")
    return False, registros[0]

def crear_sede(sede:dict):
    return repo.append_sede(sede)

def modificar_sede(id_sede:int, sede:dict):
    error, resultado = obtener_sede(id_sede)
    if error:
        return True, resultado
    return repo.actualizar_sede(id_sede, sede)

def eliminar_sede(id_sede:int):
    error, resultado = obtener_sede(id_sede)
    if error:
        return True, resultado
    error, cantidad = repo.contar_funciones_sede(id_sede)
    if error:
        return True, cantidad
    if cantidad > 0:
        return True, ERROR_CLIENTE["CONFLICT"]("La sede tiene funciones programadas, no se puede eliminar")
    return repo.eliminar_sede(id_sede)