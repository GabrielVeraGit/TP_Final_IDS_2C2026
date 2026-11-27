
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
        return utils.manejar_error(respuesta, codigo, url_for('index'))

    flash(respuesta.get("message", "Reserva realizada correctamente"), "success")
    return redirect(url_for('reserva_bp.pago', qr_id=respuesta["qr_id"]))

@reserva_bp.route("/reservas/<string:qr_id>/pago", methods=["GET"])
def pago(qr_id):
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("GET", "/reservas", params={"qr": qr_id})
    if error:
        return utils.manejar_error(respuesta, codigo, url_for('reserva_bp.mis_reservas'))
    if len(respuesta["registros"]) == 0:
        return utils.manejar_error("No existe esa reserva", 404, url_for('reserva_bp.mis_reservas'))
    reserva = respuesta["registros"][0]

    if reserva["estado_pago"] == "vencida":
        flash("El tiempo para pagar vencio, hace una nueva reserva", "error")
        return redirect(url_for('reserva_bp.mis_reservas'))
    if reserva["estado_compra"] != "reservada" or reserva["estado_pago"] == "pagada":
        flash("Esta reserva no esta pendiente de pago", "error")
        return redirect(url_for('reserva_bp.mis_reservas'))

    error, datos_qr, codigo = utils.llamar("GET", f"/reservas/{qr_id}/qr-pago")
    if error:
        return utils.manejar_error(datos_qr, codigo, url_for('reserva_bp.mis_reservas'))

    return render_template("pago.html", reserva=reserva, qr=datos_qr)


@reserva_bp.route("/reservas/<string:qr_id>/pagar", methods=["GET"])
def pagar(qr_id):
    """Es la url que abre el QR de pago: al escanearlo se hace este GET"""
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("PUT", f"/reservas/{qr_id}/pagar")
    if error:
        return utils.manejar_error(respuesta, codigo, url_for('reserva_bp.mis_reservas'))

    flash(respuesta.get("message", "Pago registrado"), "success")
    return redirect(url_for('reserva_bp.mis_reservas'))

@reserva_bp.route("/mis-reservas", methods=["GET"])
def mis_reservas():
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("GET", "/reservas")

    if error:
        return utils.manejar_error(respuesta, codigo, url_for('index'))

    reservas = respuesta.get("registros", [])

    error, respuesta, codigo = utils.llamar("GET", "/user/perfil")
    if error:

        return utils.manejar_error(respuesta, codigo, url_for('index'))

    usuario = respuesta.get("usuario", {})


    return render_template("mis_reservas.html", reservas=reservas, usuario=usuario)


@reserva_bp.route("/reservas/<string:qr_id>/cancelar", methods=["GET","POST"])
def cancelar(qr_id):
    acceso = utils.verificar_sesion("cliente")
    if acceso:
        return acceso

    error, respuesta, codigo = utils.llamar("PUT", f"/reservas/{qr_id}/cancelar")

    if error:
        return utils.manejar_error(respuesta, codigo, url_for('reserva_bp.mis_reservas'))

    flash("Reserva cancelada correctamente", "success")
    return redirect(url_for('reserva_bp.mis_reservas'))


@reserva_bp.route("/reservas/<string:qr_id>/usar", methods=["GET", "POST"])
def usar(qr_id):
    acceso = utils.verificar_sesion("admin")
    if acceso:
        return acceso
    
    qr_id_buscado=request.args.get("QR-ID", None)
    if qr_id_buscado:
        return redirect(url_for('reserva_bp.usar', qr_id=qr_id_buscado.upper()))
    
    if qr_id != "none":#si -> buscamos qr_id

        error, respuesta, codigo = utils.llamar("GET", "/reservas", params={"qr":qr_id})
        if error:
            return utils.manejar_error(respuesta, codigo, url_for('reserva_bp.usar', qr_id="none"))
        elif len(respuesta["registros"])==0:
            return utils.manejar_error("QR-ID NOT FOUND", 404, url_for('reserva_bp.usar', qr_id="none"))
        
        if request.method == "POST":
            error, respuesta, codigo = utils.llamar("PUT", f"/reservas/{qr_id}/usar")
            if error:
                return utils.manejar_error(respuesta, codigo, url_for('reserva_bp.usar', qr_id="none"))
            
            flash(f"Reserva {qr_id} fue usada!")
            return redirect(url_for('reserva_bp.usar', qr_id="none"))
        
        return render_template('check_in.html', qr_id=qr_id, registros=respuesta["registros"][0])
    else:
        return render_template('check_in.html', qr_id=qr_id)




        

