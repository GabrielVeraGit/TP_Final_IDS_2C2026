import os, requests #consumir api back
from flask import request


def consumir_api_back(metodo:str="GET", ruta:str="/api", parametros:dict=None, data_json:dict=None):
    port_back = int(os.getenv("PORT_API_BACKEND", 5001))
    protocolo = request.scheme  # 'http'
    host = request.host.split(":")[0]  # '127.0.0.1'
    url_completa = f"{protocolo}://{host}:{port_back}{ruta}"

    if parametros:
        lista_params = []
        for clave, valor in parametros.items():
            lista_params.append(f"{clave}={valor}")
        url_completa = f"{url_completa}?{'&'.join(lista_params)}"

    try:
        metodo=metodo.upper()
        if metodo in ["GET", "DELETE"]:
            respuesta = requests.request(method=metodo, url=url_completa, cookies=request.cookies)

        elif metodo in ["POST", "PUT"]:
            respuesta = requests.request(method=metodo, url=url_completa, json=data_json, cookies=request.cookies)
        else:
            return True, None  # Método HTTP no soportado


        if respuesta.ok:#la API respondió con exito (código 200-299)
            return False, respuesta #DEPENDE de lo que regrese el enpoint FIJARSE EN LA DOCUMENTACION
        else:
            return True, respuesta #me trae de errors_code.py el jsonify({"errors":lista}), code_n

    except requests.exceptions.RequestException:  # API Backend está apagada o no responde
        return True, "No se pudo conectar con el servidor"


def request_api_back(method:str="GET", ruta:str="/api", parametros:dict=None, data_json:dict=None) -> tuple[bool, dict | str]:
    """
    retorna [true, str_error] si hay un error
    ||  [false, dict] si no hubo error, contenido de dict puede cambiar
    """
    error, respuesta = consumir_api_back(method, ruta, parametros, data_json)
    if error:
        if isinstance(respuesta,str):
            return True, respuesta
        else:
            lista_errores = respuesta.json().get("errors", [])
            if lista_errores:
                error_msg = lista_errores[0].get("description", "Error desconocido")
            else:
                error_msg = "Ocurrió un error inesperado al procesar la solicitud"

            return True, error_msg
        
    if respuesta.status_code == 204 or not respuesta.content:
        return False, {}
    return False, {"data": respuesta.json(), "cookie": respuesta.cookies}



def cargar_vars_footer():
    
    return {
        "registros":{
            "Paradiso Centro":"Av. Corrientes 1234, CABA",
            "Paradiso Belgrano":"Av. Cabildo 2050, CABA",
            "Paradiso Palermo":"Av. Santa Fe 3300, CABA"
        },
    "redes_sociales":{
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "Twitter": "https://x.com",
        "youtube": "https://google.com",
        "twitch": "https://twitch.tv",
        "discord": "https://discord.com",
        "github": "https://github.com"
        },
    "soporte":{
        "Registrarse":"user_bp.registro",
        "Login":"user_bp.login"
        },
    "texto_cine":"¡Viví los mejores estrenos en pantalla gigante y con los pochoclos más ricos! ¡Sacá tus entradas hoy!",
    }