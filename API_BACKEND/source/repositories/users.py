from source.db import ejecutar_instruccion
from errors_code import ERROR_SERVIDOR

def obtener_emails_admins() -> list:
    query = "SELECT email FROM EMAILS_ADMIN"
    try:
        resultados = ejecutar_instruccion(query)
        emails_admins = list()
        for resultado in resultados:
            emails_admins.append(resultado["email"])
        return False, emails_admins
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_emails_admins, {str(e)}")

#usr debe contener nombre, apellido, email, password, rol
def append_usuarios(usr:dict):
    query = "INSERT INTO USUARIOS (nombre, apellido, email, password, rol) VALUES (%s, %s, %s, %s, %s);"
    usr_tuple=(usr["nombre"], usr["apellido"], usr["email"], usr["password"], usr["rol"])
    try:
        ejecutar_instruccion(query, usr_tuple, True)
        return False, None
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB append_usuario, {str(e)}")

#filtros: clave=alguna columna de la tabla; valor=filtros para la query, si no se manda, obtiene todos los registros
def obtener_usuarios_filtros(filtros:dict=None):
    query = f"SELECT * FROM USUARIOS"
    valores=()
    if filtros:
        columnas, valores=zip(*filtros.items())
        columnas = list(map(lambda a: f"{a}=%s", columnas))
        columnas=" AND ".join(columnas)

        query=f"{query} WHERE {columnas};"
    
    try:
        if valores:
            resultado=ejecutar_instruccion(query, valores)
        else:
            resultado=ejecutar_instruccion(query)
        return False, resultado
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_usuarios_filtros, {str(e)}")

    