import os
import requests

NOMBRE_COOKIE = "access_token_cookie"
TIMEOUT_SEG = 10

def url_api():
    puerto = os.getenv("PORT_API_BACKEND", "5001")
    return f"http://localhost:{puerto}/api"

def armar_headers():
    clave = os.getenv("API_KEY")
    if clave:
        return {"X-API-KEY": clave}
    return dict()

def descripcion_error(cuerpo, codigo:int) -> str:
    try:
        return cuerpo["errors"][0]["description"]
    except (KeyError, IndexError, TypeError):
        return f"Error {codigo} al consultar la API"

def armar_resultado(respuesta) -> tuple[bool,str|dict,int]:
    try:
        cuerpo = respuesta.json()
    except ValueError:
        cuerpo = dict()
    if respuesta.status_code >= 400:
        return True, descripcion_error(cuerpo, respuesta.status_code), respuesta.status_code
    return False, cuerpo, respuesta.status_code

def llamar_api(metodo:str, ruta:str, token:str=None, datos:dict=None, params:dict=None) -> tuple[bool,str|dict,int]:
    """Ëmpaqueta el token"""
    cookies = dict()
    if token:#empaquetar el token
        cookies[NOMBRE_COOKIE] = token
    try:
        respuesta = requests.request(metodo, url_api() + ruta, json=datos, params=params, cookies=cookies, headers=armar_headers(), timeout=TIMEOUT_SEG)
    except requests.exceptions.RequestException:
        return True, "No se pudo conectar con la API", 503
    return armar_resultado(respuesta)

def iniciar_sesion_api(email:str, password:str) -> tuple[bool,str|dict,int]:
    """Desempaqueta el token"""
    try:
        respuesta = requests.post(url_api() + "/user/login", json={"email": email, "password": password}, headers=armar_headers(), timeout=TIMEOUT_SEG)
    except requests.exceptions.RequestException:
        return True, "No se pudo conectar con la API", 503
    error, cuerpo, codigo = armar_resultado(respuesta)
    if error:
        return True, cuerpo, codigo
    return False, respuesta.cookies.get(NOMBRE_COOKIE), codigo#desempaquetar token

