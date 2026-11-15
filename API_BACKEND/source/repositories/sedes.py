from source.db import ejecutar_instruccion, ejecutar_insercion
from errors_code import ERROR_SERVIDOR

def obtener_sedes():
    query = "SELECT id_sede, nombre, direccion FROM SEDES ORDER BY nombre;"
    try:
        return False, ejecutar_instruccion(query)
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_sedes, {str(e)}")

def obtener_sede(id_sede:int):
    query = "SELECT id_sede, nombre, direccion FROM SEDES WHERE id_sede = %s;"
    try:
        return False, ejecutar_instruccion(query, (id_sede,))
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_sede, {str(e)}")

def append_sede(sede:dict):
    query = "INSERT INTO SEDES (nombre, direccion) VALUES (%s, %s);"
    try:
        id_sede = ejecutar_insercion(query, (sede["nombre"], sede["direccion"]))
        return False, id_sede
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB append_sede, {str(e)}")

def actualizar_sede(id_sede:int, sede:dict):
    query = "UPDATE SEDES SET nombre = %s, direccion = %s WHERE id_sede = %s;"
    try:
        ejecutar_instruccion(query, (sede["nombre"], sede["direccion"], id_sede), True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB actualizar_sede, {str(e)}")

def eliminar_sede(id_sede:int):
    query = "DELETE FROM SEDES WHERE id_sede = %s;"
    try:
        ejecutar_instruccion(query, (id_sede,), True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB eliminar_sede, {str(e)}")

def contar_funciones_sede(id_sede:int):
    query = """SELECT COUNT(*) AS cantidad
               FROM FUNCIONES F
               JOIN SALAS S ON S.id_sala = F.id_sala
               WHERE S.id_sede = %s;"""
    try:
        return False, ejecutar_instruccion(query, (id_sede,))[0]["cantidad"]
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB contar_funciones_sede, {str(e)}")