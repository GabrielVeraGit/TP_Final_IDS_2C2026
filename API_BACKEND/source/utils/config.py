import os
from dotenv import load_dotenv

load_dotenv()
#Clave compartida entre el aplicativo front y la API
API_KEY = os.getenv("API_KEY", "")

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
OMDB_URL = "https://www.omdbapi.com/"

URL_FRONTEND = "http://localhost:" + os.getenv("PORT_APLICATIVO_FRONTEND", "5002")

HORAS_DURACION_SESION = 24
HORAS_LIMITE_CANCELACION = 2
MAX_ENTRADAS_POR_RESERVA = 10
MINUTOS_ANTES_VALIDACION_QR = 60
MINUTOS_DESPUES_VALIDACION_QR = 30
MINUTOS_ENTRE_FUNCIONES = 15
DURACION_POR_DEFECTO_MIN = 120



