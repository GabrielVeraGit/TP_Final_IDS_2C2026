from flask import Blueprint, jsonify
from errors_code import ERROR_CLIENTE
from source import extend_jwt, extend_qr, extend_email

from source.validators import reservas as val
from source.services import reservas as serv
from source.repositories import reservas as repo

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/reservas', methods=['GET'])
@extend_jwt.seguro()
def get_reservas():
    error, qp_limpios = val.validando_query_paramts()
    if error:
        return qp_limpios
    
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    if data_extra["rol"] == "cliente":
        qp_limpios["id_usuario"] = data_extra["id_usuario"]

    error, respuesta = serv.confirmando_query_paramts(qp_limpios)
    if error:
        return respuesta
    
    error, registros = repo.obtener_reservas_filtros(qp_limpios)
    if error:
        return registros
    return jsonify({"registros":registros}), 200

@reserva_bp.route('/reservas/<int:id_reserva>', methods=['GET'])
@extend_jwt.seguro()
def get_reserva(id_reserva:int):
    filtros = {"id_reserva":id_reserva}
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    if data_extra["rol"] == "cliente":
        filtros["id_usuario"] = data_extra["id_usuario"]
    
    error, registros = repo.obtener_reservas_filtros(filtros)
    if error:
        return registros
    if len(registros) == 0:
        return ERROR_CLIENTE["NOT_FOUND"](f"La reserva {id_reserva} no existe")
    return jsonify({"registros":registros}), 200


@reserva_bp.route('/reservas', methods=['POST'])
@extend_jwt.seguro()
def create_reserva():
    error, result = extend_jwt.verificar_rol_permitido("cliente")
    if error:
        return result
    
    error, body_limpio = val.validando_json()
    if error:
        return body_limpio

    error, respuesta = serv.confirmando_json(body_limpio)
    if error:
        return respuesta
    error, registro = serv.confirmando_reserva(body_limpio)
    if error:
        return registro
    
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    
    body_limpio["id_usuario"]=data_extra["id_usuario"]

    qr_id = extend_qr.generar_qr_id()
    error, respuesta = repo.crear_reserva(body_limpio, qr_id)
    if error:
        return respuesta

    return jsonify({"message": "Reserva registrada, falta el pago", "qr_id": qr_id}), 201


@reserva_bp.route('/reservas/<string:qr_id>/qr-pago', methods=['GET'])
@extend_jwt.seguro()
def get_qr_pago(qr_id:str):
    error, result = extend_jwt.verificar_rol_permitido("cliente")
    if error:
        return result
    error, registro = serv.confirmando_pendiente_de_pago(qr_id)
    if error:
        return registro
    url_usar, url_cancelar, url_pagar = extend_qr.armar_urls(qr_id)
    return jsonify({"qr_id": qr_id,
                    "url_pago": url_pagar,
                    "segundos_restantes": serv.calcular_segundos_restantes(registro),
                    "qr_base64": extend_qr.generar_qr_base64(url_pagar)}), 200


@reserva_bp.route('/reservas/<string:qr_id>/pagar', methods=['PUT'])
@extend_jwt.seguro()
def pagar_reserva(qr_id:str):
    error, result = extend_jwt.verificar_rol_permitido("cliente")
    if error:
        return result
    error, registro = serv.confirmando_pago(qr_id)
    if error:
        return registro
    error, result = repo.pagar_reserva(registro, qr_id)
    if error:
        return result

    identificador, data_extra = extend_jwt.obtener_informacion_token()
    url_usar, url_cancelar, url_pagar = extend_qr.armar_urls(qr_id)
    qr_buffer = extend_qr.generar_qr_en_memoria(url_usar)
    error, result = extend_email.send_reserva(qr_id, url_cancelar, qr_buffer, identificador, registro)
    if error:
        return jsonify({"message": "Pago registrado, pero no se pudo enviar el mail"}), 200
    return jsonify({"message": "Pago registrado, revise su bandeja de entrada"}), 200


@reserva_bp.route('/reservas/<string:qr_id>/cancelar', methods=['PUT'])
@extend_jwt.seguro()
def cancelar_reserva(qr_id:str):
    error, result = extend_jwt.verificar_rol_permitido("cliente")
    if error:
        return result
    error, registro = serv.confirmando_cancelacion(qr_id)
    if error:
        return registro
    error, result = repo.cancelar_reserva(registro, qr_id)
    if error:
        return result
    return jsonify({"message": "Reserva cancelada"}), 200


@reserva_bp.route('/reservas/<string:qr_id>/usar', methods=['PUT'])
@extend_jwt.seguro()
def usar_reserva(qr_id:str):
    error, result = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return result
    error, registro = serv.confirmando_uso(qr_id)
    if error:
        return registro
    error, result = repo.usar_reserva(registro, qr_id)
    if error:
        return result    
    return jsonify({"message": "Reserva usada"}), 200