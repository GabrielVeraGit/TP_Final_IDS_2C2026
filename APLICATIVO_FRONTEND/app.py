import os
from dotenv import load_dotenv
from flask import Flask, request, flash, render_template
from source import formato, utils, API
from source.config import SEDES
from source.routes.users import user_bp
from source.routes.peliculas import pelicula_bp
from source.routes.reservas import reserva_bp
#from source.admin import admin_bp
#saquen el # cuando hayan creado el archivo y su bp!

load_dotenv()

app  = Flask(__name__)
app.secret_key = os.getenv("FRONT_SECRET_KEY", "clave_del_aplicativo_tp")

app.register_blueprint(user_bp, url_prefix="/cine_paradiso")
app.register_blueprint(pelicula_bp, url_prefix="/cine_paradiso")
app.register_blueprint(reserva_bp, url_prefix="/cine_paradiso")

#lo mismo aca
app.add_template_filter(formato.filtro_fecha, "fecha")
app.add_template_filter(formato.filtro_dia_corto, "dia_corto")
app.add_template_filter(formato.filtro_hora, "hora")
app.add_template_filter(formato.filtro_dinero, "dinero")




@app.route("/cine_paradiso", methods=["GET"])
def index():
    redireccion = utils.verificar_sesion()
    if redireccion:
        return redireccion
    params = utils.tomar_campos(request.args, ("titulo", "genero"))
    error, peliculas, codigo = utils.llamar("GET", "/peliculas/cartelera", params=params)
    if error:
        flash(peliculas, "error")
        peliculas = []
    return render_template("index.html", peliculas=peliculas, filtros=params)



@app.context_processor
def inyectar_seccion():
    seccion = "cartelera"
    if request.path == "/cine_paradiso":
        seccion = "inicio"
    elif request.path.startswith("/cine_paradiso/admin"):
        seccion = "admin"
    elif request.path.endswith("/usar"):
        seccion = "checkin"
    elif request.path.startswith("/cine_paradiso/mis-reservas") or request.path.startswith("/cine_paradiso/comprar") or request.path.endswith("/cine_paradiso/cancelar"):
        seccion = "reservas"
    elif request.path.startswith("/cine_paradiso/perfil"):
        seccion = "perfil"
    return dict(seccion=seccion, sedes_cine=SEDES)

if __name__ == "__main__":
    puerto = int(os.getenv("PORT_APLICATIVO_FRONTEND", 5002))
    app.run(port=puerto, host="0.0.0.0", debug=True)