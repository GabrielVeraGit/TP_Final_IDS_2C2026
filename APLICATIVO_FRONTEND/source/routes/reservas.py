
from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from source import utils

reserva_bp = Blueprint("reserva_bp", __name__)


@reserva_bp.route("/comprar/<int:id_funcion>", methods=["POST"])
def comprar(id_funcion):
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    try:
        cantidad = int(request.form.get("cant_entradas", 0))
    except ValueError:
        cantidad = 0

    if cantidad < 1 or cantidad > 10:
        flash("Cantidad de entradas invalida", "error")
        return redirect(url_for('index'))

    datos = {
        "id_funcion": id_funcion,
        "cant_entradas": cantidad
    }

    error, respuesta, codigo = utils.llamar("POST", "/reservas", datos=datos)

    if error:
        return utils.manejar_error(respuesta, codigo, "/")

    flash(respuesta.get("message", "Reserva realizada correctamente"), "success")
    return redirect(url_for('index'))

@reserva_bp.route("/mis-reservas")
def mis_reservas():
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("GET", "/reservas")

    if error:
        return utils.manejar_error(respuesta, codigo, "/")

    reservas = respuesta.get("registros", [])

    return render_template("mis_reservas.html", reservas=reservas)


@reserva_bp.route("/reservas/<string:qr_id>/cancelar", methods=["GET","POST"])
def cancelar(qr_id):
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("PUT", f"/reservas/{qr_id}/cancelar")

    if error:
        return utils.manejar_error(respuesta, codigo, "/mis-reservas")

    flash("Reserva cancelada correctamente", "success")
    return redirect(url_for('reserva_bp.mis_reservas'))


    
@reserva_bp.route("/reservas/<string:qr_id>/usar", methods=["GET","POST"])#falta
def cancelar(qr_id):
    acceso = utils.verificar_sesion("admin")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("PUT", f"/reservas/{qr_id}/usar")

    if error:
        return utils.manejar_error(respuesta, codigo, "/mis-reservas")

    flash("Reserva cancelada correctamente", "success")
    return redirect(url_for('reserva_bp.mis_reservas'))