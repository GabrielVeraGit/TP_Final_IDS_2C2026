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

#obtiene los usuarios(todas las columnas), con filtros de registros "WHERE id_usuario > 4 AND ..."
#filtros: clave=la columna filtro; valor=el dato filtro
def obtener_usuarios_filtros(filtros:dict=None, con_password:bool=False)-> list[dict]:
    if con_password:
        query = f"SELECT * FROM USUARIOS"
    else:
        query = f"SELECT id_usuario, nombre, apellido, email, rol FROM USUARIOS"
    valores=()
    if filtros:
        columnas, valores=zip(*filtros.items())
        columnas = list(map(lambda a: f"{a}=%s", columnas))
        columnas=" AND ".join(columnas)

        query=f"{query} WHERE {columnas};"
    else:
        query=f"{query};"
        
    try:
        if valores:
            resultado=ejecutar_instruccion(query, valores)
        else:
            resultado=ejecutar_instruccion(query)
        return False, resultado
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_usuarios_filtros, {str(e)}")

def obtener_resumen_consumos(id_usuario: int) -> dict:
    query = """SELECT COUNT(*) AS cantidad_compras,
                      CAST(COALESCE(SUM(cant_entradas), 0) AS SIGNED) AS entradas_compradas,
                      COALESCE(SUM(monto_a_pagar), 0) AS total_gastado
               FROM RESERVAS
               WHERE id_usuario = %s AND estado_compra <> 'cancelada'"""
    return ejecutar_instruccion(query, (id_usuario,))[0]

def obtener_peliculas_vistas(id_usuario: int) -> list[dict]:
    query = """SELECT P.id_pelicula, P.titulo, P.poster, P.genero,
                      MAX(F.fecha_hora) AS ultima_vez_vista,
                      COUNT(DISTINCT F.id_funcion) AS veces_vista
               FROM RESERVAS R
               JOIN FUNCIONES F ON F.id_funcion = R.id_funcion
               JOIN PELICULAS P ON P.id_pelicula = F.id_pelicula
               WHERE R.id_usuario = %s
                 AND (R.estado_compra = 'usada'
                      OR (R.estado_compra = 'reservada' AND F.fecha_hora < NOW()))
               GROUP BY P.id_pelicula, P.titulo, P.poster, P.genero
               ORDER BY ultima_vez_vista DESC"""
    return ejecutar_instruccion(query, (id_usuario,))

    