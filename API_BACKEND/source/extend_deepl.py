import requests, json, os
from errors_code import ERROR_SERVIDOR

DEEPL_API_KEY=str(os.getenv("DEEPL_API_KEY"))


def consumir_api_deepl(texto_traducir:str):
    url="https://api-free.deepl.com/v2/translate"
    headers={
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/json"
        }
    body={
    "text": [texto_traducir],
    "target_lang": "ES"
    }

    try:
       
        respuesta=requests.post(url=url, headers=headers, json=body)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return False, datos['translations'][0]['text']
    except requests.exceptions.RequestException as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error comunicacion, deepl: {str(e)}")
    
