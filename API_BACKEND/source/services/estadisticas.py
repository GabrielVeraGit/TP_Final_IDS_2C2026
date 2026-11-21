from source.repositories import estadisticas as repo


def obtener_ocupacion_funciones():
    return repo.obtener_ocupacion_funciones()


def obtener_ventas_por_genero():
    return repo.obtener_ventas_por_genero()
