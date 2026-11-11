import os
from dotenv import load_dotenv
from flask import Flask
from source.routes.users import user_bp
from source.routes.peliculas import pelicula_bp
from source.routes.sedes import sede_bp
from source.routes.funciones import funcion_bp
from source.routes.salas import sala_bp
from source.routes.reservas import reserva_bp

load_dotenv()

app  = Flask(__name__)


app.register_blueprint(user_bp,     url_prefix="/api")
app.register_blueprint(pelicula_bp, url_prefix="/api")
app.register_blueprint(sede_bp,     url_prefix="/api")
app.register_blueprint(funcion_bp,  url_prefix="/api")
app.register_blueprint(sala_bp,     url_prefix="/api")
app.register_blueprint(reserva_bp,  url_prefix="/api")
@app.route("/api", methods=["GET"])
def index():
    return "ENTRASTE A LA API", 200


if __name__ == "__main__":
    puerto=int(os.getenv("PORT_API_BACKEND", 5001))
    app.run(port=puerto, debug=False)
