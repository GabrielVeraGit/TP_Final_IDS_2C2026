import os
from dotenv import load_dotenv
from flask import Flask
from source.routes.users import user_bp
from source.route.peliculas import pelicula_bp
from source.route.sedes import sedes_bp
from source.route.funciones import funcion_bp
from source.route.salas import salas_bp

load_dotenv()

app  = Flask(__name__)


app.register_blueprint(user_bp)
app.register_blueprint(pelicula_bp)
app.register_blueprint(sedes_bp)
app.register_blueprint(funcion_bp)
app.register_blueprint(salas_bp)

@app.route("/api", methods=["GET"])
def index():
    return "ENTRASTE A LA API", 200


if __name__ == "__main__":
    puerto=int(os.getenv("PORT_API_BACKEND", 5001))
    app.run(port=puerto, debug=False)
