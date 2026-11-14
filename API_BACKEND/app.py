import os
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
from flask import Flask

from werkzeug.exceptions import HTTPException
from source import extend_email, extend_jwt

from source.routes.users import user_bp
from source.routes.peliculas import pelicula_bp
from source.routes.sedes import sede_bp
from source.routes.funciones import funcion_bp
from source.routes.salas import sala_bp
from source.routes.reservas import reserva_bp

from errors_code import ERROR_CLIENTE, ERROR_SERVIDOR
from source.auth import verificar_api_key

load_dotenv()

app  = Flask(__name__)

#Configuracion json
def convertir_a_json(valor):
    if isinstance(valor, datetime):
        return valor.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(valor, Decimal):
        return float(valor)
    return str(valor)

app.json.default = convertir_a_json
app.json.sort_keys = False
app.json.ensure_ascii = False

# Configuración Mail 
extend_email.config(app)

#Configuracion Tokens
extend_jwt.config(app)

# Blueprints
app.register_blueprint(user_bp,     url_prefix="/api")
app.register_blueprint(pelicula_bp, url_prefix="/api")
app.register_blueprint(sede_bp,     url_prefix="/api")
app.register_blueprint(funcion_bp,  url_prefix="/api")
app.register_blueprint(sala_bp,     url_prefix="/api")
app.register_blueprint(reserva_bp,  url_prefix="/api")

#Api externa
#app.before_request(verificar_api_key)
    
@app.errorhandler(HTTPException)
def manejar_error_http(error:HTTPException):
    if error.code == 404:
        return ERROR_CLIENTE["NOT_FOUND"](error.description)
    if error.code == 405:
        return ERROR_CLIENTE["METHOD_NOT_ALLOWED"](error.description)
    return ERROR_CLIENTE["BAD_REQUEST"](error.description)

@app.errorhandler(Exception)
def manejar_error_interno(error:Exception):
    print(f"Error interno: {error}")
    return ERROR_SERVIDOR["INTERNAL_SERVER_ERROR"]("Error interno del servidor")


@app.route("/api", methods=["GET"])
def index():
    return "ENTRASTE A LA API", 200


if __name__ == "__main__":
    puerto=int(os.getenv("PORT_API_BACKEND", 5001))
    app.run(port=puerto, debug=False)
