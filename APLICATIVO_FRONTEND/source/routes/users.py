from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from source import API
from source import utils

user_bp = Blueprint("user_bp", __name__)

#usuarios 
@user_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")
    
    datos = utils.tomar_campos(request.form, ("nombre", "apellido", "email", "password"))
    datos["password"]=request.form.get("password")
    error, cuerpo, codigo = API.llamar_api("POST", "/user/register", None, datos)

    if error:
        flash(cuerpo, "error")
        return render_template("registro.html")
    
    flash(cuerpo["message"], "ok")
    return redirect(url_for("user_bp.login"))

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    siguiente = request.values.get("siguiente", "")
    if request.method == "GET":
        return render_template("login.html", siguiente=siguiente)

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    error, token, codigo = API.iniciar_sesion_api(email, password)

    if error:
        flash(token, "error")
        return render_template("login.html", siguiente=siguiente)

    rol = utils.obtener_rol(token)
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

@user_bp.route("/logout", methods=["POST"])
def logout():
    if utils.token_sesion():
        utils.llamar("POST", "/user/logout")
    session.clear()
    flash("Sesion cerrada", "ok")
    return redirect(url_for("index"))


@user_bp.route("/perfil", methods=["GET"])
def perfil():
    
    return redirect(url_for("index"))

@user_bp.route("/admin", methods=["GET"])
def admin():
    return redirect(url_for("index"))

@user_bp.route("/new_admin", methods=["GET", "POST"])
def new_admin():
    acceso = utils.verificar_sesion("admin")
    if acceso:
        return acceso
    
    request_json=dict()
    if request.method == "POST":
        request_json["email"]=session["email"]
        request_json["password"]=request.form.get("password")
        request_json["new_email"]=request.form.get("new_email")
        
        error, respuesta, codigo = utils.llamar("POST", "/emails-admin", request_json)
        if error:
            return utils.manejar_error(respuesta, codigo, url_for('user_bp.new_admin'))

        flash(f"Nuevo email admin {request_json["new_email"]} registrado!")
        return redirect(url_for('user_bp.new_admin'))
    else:
        return render_template('new_admin.html')