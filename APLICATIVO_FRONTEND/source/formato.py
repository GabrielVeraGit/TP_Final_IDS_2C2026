from datetime import datetime
from source.config import DIAS_SEMANA, MESES

def leer_fecha(texto:str):
    try:
        return datetime.strptime(str(texto)[:16], "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def filtro_fecha(texto):
    fecha = leer_fecha(texto)
    if fecha is None:
        return texto
    return f"{DIAS_SEMANA[fecha.weekday()]} {fecha.day} {MESES[fecha.month - 1]} - {fecha.strftime('%H:%M')}"

def filtro_dia_corto(texto):
    fecha = leer_fecha(texto)
    if fecha is None:
        return texto
    return f"{DIAS_SEMANA[fecha.weekday()]} {fecha.day} {MESES[fecha.month - 1]}"

def filtro_hora(texto):
    fecha = leer_fecha(texto)
    if fecha is None:
        return texto
    return fecha.strftime("%H:%M")

def filtro_dinero(valor):
    texto = f"{float(valor or 0):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    if texto.endswith(",00"):
        texto = texto[:-3]
    return "$ " + texto