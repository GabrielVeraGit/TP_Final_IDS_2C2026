from flask import request, redirect, url_for, session, flash
from source.llamadas_api import llamar_api
from source.config import DESDE_SIEMPRE

def token_sesion():
    return session.get("token")

def llamar(metodo:str, ruta:str, datos:dict=None, params:dict=None):
    return llamar_api(metodo, ruta, token_sesion(), datos, params)

def tomar_campos(origen, campos:tuple):
    datos = dict()
    for campo in campos:
        valor = origen.get(campo, "").strip()
        if valor != "":
            datos[campo] = valor
    return datos


def verificar_sesion(rol:str=None):
    if not token_sesion():
        flash("Inicia sesion para continuar", "error")
        return redirect(url_for("usuarios_bp.login", siguiente=request.path))
    if rol and session.get("rol") != rol:
        flash(f"Esa pagina es solo para {rol}", "error")
        return redirect(url_for("cartelera_bp.index"))
    return None

def manejar_error(mensaje:str, codigo:int, destino:str):
    if codigo == 401:
        session.clear()
        flash("Tu sesion vencio, inicia sesion de nuevo", "error")
        return redirect(url_for("usuarios_bp.login"))
    flash(mensaje, "error")
    return redirect(destino)

def obtener_rol(token:str):
    error, cuerpo, codigo = llamar_api("GET", "/user/perfil", token)
    if codigo == 403:
        return "admin"
    if error:
        return None
    return "cliente"

def funciones_por_id():
    error, funciones, codigo = llamar("GET", "/funciones", params={"desde": DESDE_SIEMPRE})
    por_id = dict()
    if error:
        return por_id
    for f in funciones:
        por_id[f["id_funcion"]] = f
    return por_id