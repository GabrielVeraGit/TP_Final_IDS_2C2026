import os
from flask import Blueprint, request, render_template, make_response, redirect, url_for
from source import utils, extend_jwt
user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/register", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        datos_usuario = {
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "email": request.form.get("email"),
        "password": request.form.get("password")}

            
        error, respuesta = utils.request_api_back("POST", "/api/user/register", data_json=datos_usuario)
        if error:
            return render_template('formulario_registro.html', error=respuesta)
        data=respuesta["data"]
        

        resp_registrado=data.get("message")
        return render_template('formulario_registro.html', exito=resp_registrado)
          
    else:
        return render_template('formulario_registro.html')

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        datos_usuario = {
        "email": request.form.get("email"),
        "password": request.form.get("password")}

        
        error, respuesta = utils.request_api_back("POST", "/api/user/login", data_json=datos_usuario)
        if error:
            return render_template('formulario_login.html', error=respuesta)
        data=respuesta["data"]
        cookies=respuesta["cookie"]


        html_exito = make_response(render_template('formulario_login.html', exito=True))
        for cookie in cookies:
            html_exito.set_cookie(
                key=cookie.name,
                value=cookie.value,
                expires=cookie.expires,
                httponly=True,  # Protege la cookie contra JavaScript malicioso
                samesite='Lax'  # Evita problemas de bloqueo en el navegador
            )

        return html_exito
          
    else:
        return render_template('formulario_login.html')

@user_bp.route("/logout", methods=["POST"])
@extend_jwt.seguro()
def logout():
    error, respuesta = utils.request_api_back("POST", "/api/user/logout")
    if error:
        # Ojo: si login está en el blueprint, debe ser 'user_bp.login'
        resp = make_response(redirect(url_for('user_bp.login')))
    else:
        resp = make_response(redirect(url_for('index')))
        
    # Le pegamos la orden de borrar la cookie a la redirección hacia el navegador
    return extend_jwt.eliminar_cookie(resp)