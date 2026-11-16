from errors_code import ERROR_SERVIDOR
from source.db import ejecutar_instruccion

#filtros: clave=la columna filtro; valor=el dato filtro
def obtener_reservas_filtros(filtros:dict=None)-> list[dict]:
    query = "SELECT * FROM RESERVAS"
    if filtros:
        filtros_c = filtros.copy()
    else:
        filtros_c = dict()
    
    condiciones = []
    valores = []

    date1 = filtros_c.pop("fecha_desde", None)
    date2 = filtros_c.pop("fecha_hasta", None)

    if date1 is not None and date2 is not None:
        condiciones.append("fecha_de_compra BETWEEN %s AND %s")
        valores.extend([date1, date2])
    elif date1 is not None:
        condiciones.append("fecha_de_compra >= %s")
        valores.append(date1)
    elif date2 is not None:
        condiciones.append("fecha_de_compra <= %s")
        valores.append(date2)

    for columna, valor in filtros_c.items():
        condiciones.append(f"{columna} = %s")
        valores.append(valor)

    if condiciones:
        union_col = " AND ".join(condiciones)
        query = f"{query} WHERE {union_col};"
    else:
        query = f"{query};"

    try:
        if valores:
            resultado = ejecutar_instruccion(query, tuple(valores))
        else:
            resultado = ejecutar_instruccion(query)
        return False, resultado
    except Exception as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error DB obtener_reservas_filtros, {str(e)}")

