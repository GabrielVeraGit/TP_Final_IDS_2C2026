
from flask import Blueprint, request, redirect, url_for, flash, render_template
from source.utils import llamar, verificar_sesion, manejar_error

reservas_bp = Blueprint("reservas_bp", __name__)


@reservas_bp.route("/comprar/<int:id_funcion>", methods=["POST"])
def comprar(id_funcion):
    acceso = verificar_sesion("cliente")
    if acceso:
        return acceso

    try:
        cantidad = int(request.form.get("cant_entradas", 0))
    except ValueError:
        cantidad = 0

    if cantidad < 1 or cantidad > 10:
        flash("Cantidad de entradas invalida", "error")
        return redirect("/")

    datos = {
        "id_funcion": id_funcion,
        "cant_entradas": cantidad
    }

    error, respuesta, codigo = llamar("POST", "/reservas", datos=datos)

    if error:
        return manejar_error(respuesta, codigo, "/")

    flash(respuesta.get("message", "Reserva realizada correctamente"), "success")
    return redirect("/")

@reservas_bp.route("/mis-reservas")
def mis_reservas():
    acceso = verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = llamar("GET", "/reservas")

    if error:
        return manejar_error(respuesta, codigo, "/")

    reservas = respuesta.get("registros", [])

    return render_template("mis_reservas.html", reservas=reservas)


@reservas_bp.route("/reservas/<string:qr_id>/cancelar", methods=["POST"])
def cancelar(qr_id):
    acceso = verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = llamar(
        "PUT",
        f"/reservas/{qr_id}/cancelar"
    )

    if error:
        return manejar_error(respuesta, codigo, "/mis-reservas")

    flash("Reserva cancelada correctamente", "success")
    return redirect("/mis-reservas")

