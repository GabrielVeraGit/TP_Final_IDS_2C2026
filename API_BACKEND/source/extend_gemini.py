import requests, json, os
from errors_code import ERROR_SERVIDOR, ERROR_CLIENTE

GEMINI_API_KEY=str(os.getenv("GEMINI_API_KEY"))

def consumir_api_gemini(descripcion_peli:str) -> tuple[bool, dict]:
    """{'titulo_original': None, 'anio': None}"""
    
    url = "https://generativelanguage.googleapis.com/v1beta/interactions"

    prompt_sistema ="""
    Eres un experto en cine. Recibirás la descripción informal de una
    película. Devuelve ÚNICAMENTE un objeto JSON válido con dos claves:
    'titulo_original' (titulo en el nombre oficial que se dio en el idioma ingles) y 'anio' (entero). Tomando en cuenta que solo devolveras
    la primera entrega si pertenece a una saga, a menos que explicitamente se mensione la otra parte o secuela.
    Si no estás seguro o no existe, devuelve null en ambos campos."""
  
    headers = {
      "x-goog-api-key": GEMINI_API_KEY,
      "Content-Type": "application/json",
    }

    body = {
    "model": "gemini-3.5-flash-lite",
    "system_instruction":prompt_sistema,
    "input": descripcion_peli,
    "response_format":{
      "type": "text",
      "mime_type": "application/json",
      "schema":{
            "type": "object",
            "properties": {
                    "titulo_original": {"type": ["string", "null"]},
                    "anio": {"type": ["integer", "null"]},
            }
      }
    },
    "generation_config": {"temperature": 0.1}
    }

    try:
    
        respuesta = requests.post(url, headers=headers, json=body)
        respuesta.raise_for_status()
        respuesta = json.loads(respuesta.json()["steps"][1]["content"][0]["text"])
        if not respuesta['titulo_original']:
            return True, ERROR_CLIENTE["NOT_FOUND"]("La pelicula no fue reconocida, gm")
        return False, respuesta
    except requests.exceptions.RequestException as e:
        return True, ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"](f"Error comunicacion, gm: {str(e)}")