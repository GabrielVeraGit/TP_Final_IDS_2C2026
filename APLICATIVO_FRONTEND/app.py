import os
from dotenv import load_dotenv
from flask import Flask, request
from source import formato
from source.config import SEDES
#from source.usuarios import usuarios_bp
#from source.cartelera import cartelera_bp
from source.reservas import reservas_bp
#from source.admin import admin_bp
#saquen el # cuando hayan creado el archivo y su bp!

load_dotenv()

app  = Flask(__name__)
app.secret_key = os.getenv("FRONT_SECRET_KEY", "clave_del_aplicativo_tp")

#app.register_blueprint(usuarios_bp)
#app.register_blueprint(cartelera_bp)
app.register_blueprint(reservas_bp)
#app.register_blueprint(admin_bp)
#lo mismo aca
app.add_template_filter(formato.filtro_fecha, "fecha")
app.add_template_filter(formato.filtro_dia_corto, "dia_corto")
app.add_template_filter(formato.filtro_hora, "hora")
app.add_template_filter(formato.filtro_dinero, "dinero")

@app.context_processor
def inyectar_seccion():
    seccion = "cartelera"
    if request.path == "/":
        seccion = "inicio"
    elif request.path.startswith("/admin") or request.path.endswith("/usar"):
        seccion = "admin"
    elif request.path.startswith("/mis-reservas") or request.path.startswith("/comprar") or request.path.endswith("/cancelar"):
        seccion = "reservas"
    elif request.path.startswith("/perfil"):
        seccion = "perfil"
    return dict(seccion=seccion, sedes_cine=SEDES)

if __name__ == "__main__":
    puerto = int(os.getenv("PORT_APLICATIVO_FRONTEND", 5002))
    app.run(port=puerto, debug=False)