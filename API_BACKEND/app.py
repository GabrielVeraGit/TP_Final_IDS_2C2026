import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from source.routes.users import user_bp
from source.routes.peliculas import pelicula_bp
from source.routes.sedes import sede_bp
from source.routes.funciones import funcion_bp
from source.routes.salas import sala_bp
from source.routes.reservas import reserva_bp

load_dotenv()

app  = Flask(__name__)

# Configuración de Flask-Mail (Tu motor de envíos)
app.config['MAIL_SERVER'] = os.getenv("EMAIL_DOMINIO_REMITENTE")
app.config['MAIL_PORT'] = int(os.getenv("EMAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_REMITENTE")
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD_REMITENTE") 
app.config['MAIL_DEFAULT_SENDER'] = (os.getenv("DB_NAME"), os.getenv("EMAIL_REMITENTE"))
#Inicializar el motor
mail = Mail(app)

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
