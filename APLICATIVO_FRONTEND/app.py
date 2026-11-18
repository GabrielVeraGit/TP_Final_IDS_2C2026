import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from llamadas_api import llamar_api, iniciar_sesion_api

load_dotenv()

app  = Flask(__name__)
app.secret_key = os.getenv("FRONT_SECRET_KEY", "clave_del_aplicativo_tp")

def token_sesion():
    return session.get("token")

def llamar(metodo:str, ruta:str, datos:dict=None, params:dict=None):
    return llamar_api(metodo, ruta, token_sesion(), datos, params)

def tomar_campos(origen, campos:tuple):
    datos = dict()
    for campo in campos:
        valor = origen.get(campo, "").strip()
        if valor != "":
            datos[campo] = valor
    return datos

#retorna None si el usuario puede entrar, o la redireccion al login si no 
def verificar_sesion(rol:str=None):
    if not token_sesion():
        if request.path != "/":
            flash("Inicia sesion para continuar", "error")
        return redirect(url_for("login", siguiente=request.path))
    if rol and session.get("rol") != rol:
        flash(f"Esa pagina es solo para {rol}", "error")
        return redirect(url_for("index"))
    return None

#muestra el error de la API y vuelve a "destino", si el token vencio manda al login
def manejar_error(mensaje:str, codigo:int, destino:str):
    if codigo == 401:
        session.clear()
        flash("Tu sesion vencio, inicia sesion de nuevo", "error")
        return redirect(url_for("login"))
    flash(mensaje, "error")
    return redirect(destino)

def obtener_rol(token:str):
    error, cuerpo, codigo = llamar_api("GET", "/user/perfil", token)
    if codigo == 403:
        return "admin"
    if error:
        return None
    return "cliente"

#cartelera 

@app.route("/", methods=["GET"])
def index():
    redireccion = verificar_sesion()
    if redireccion:
        return redireccion
    params = tomar_campos(request.args, ("titulo", "genero"))
    error, peliculas, codigo = llamar("GET", "/peliculas/cartelera", params=params)
    if error:
        flash(peliculas, "error")
        peliculas = []
    return render_template("index.html", peliculas=peliculas, filtros=params)

@app.route("/pelicula/<int:id_pelicula>", methods=["GET"])
def pelicula(id_pelicula:int):
    redireccion = verificar_sesion()
    if redireccion:
        return redireccion
    error, datos_pelicula, codigo = llamar("GET", f"/peliculas/{id_pelicula}")
    if error:
        return manejar_error(datos_pelicula, codigo, url_for("index"))
    error, funciones, codigo = llamar("GET", "/funciones", params={"id_pelicula": id_pelicula})
    if error:
        flash(funciones, "error")
        funciones = []
    return render_template("pelicula.html", pelicula=datos_pelicula, funciones=funciones)


#usuarios 

@app.route("/login", methods=["GET", "POST"])
def login():
    siguiente = request.values.get("siguiente", "")
    if request.method == "GET":
        return render_template("login.html", siguiente=siguiente)

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    error, token, codigo = iniciar_sesion_api(email, password)
    if error:
        flash(token, "error")
        return render_template("login.html", siguiente=siguiente)

    rol = obtener_rol(token)
    if rol is None:
        flash("No se pudo obtener el rol del usuario", "error")
        return render_template("login.html", siguiente=siguiente)

    session["token"] = token
    session["rol"] = rol
    session["email"] = email
    flash(f"Bienvenido/a {email}", "ok")
    if siguiente.startswith("/") and not siguiente.startswith("//"):
        return redirect(siguiente)
    return redirect(url_for("index"))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")
    datos = tomar_campos(request.form, ("nombre", "apellido", "email", "password"))
    datos["password"] = request.form.get("password", "")
    error, cuerpo, codigo = llamar_api("POST", "/user/register", None, datos)
    if error:
        flash(cuerpo, "error")
        return render_template("registro.html")
    flash(cuerpo["message"], "ok")
    return redirect(url_for("login"))

@app.route("/logout", methods=["POST"])
def logout():
    if token_sesion():
        llamar("POST", "/user/logout")
    session.clear()
    flash("Sesion cerrada", "ok")
    return redirect(url_for("index"))

if __name__ == "__main__":
    puerto = int(os.getenv("PORT_APLICATIVO_FRONTEND", 5002))
    app.run(port=puerto, debug=False)