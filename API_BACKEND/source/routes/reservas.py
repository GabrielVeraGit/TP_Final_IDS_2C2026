from flask import Blueprint, jsonify
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
    error, result = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return result
    
    error, registros = repo.obtener_reservas_filtros({"id_reserva":id_reserva})
    if error:
        return registros
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

    qr_id, url_usar, url_cancelar = extend_qr.generar_code_y_urls()
    qr_buffer = extend_qr.generar_qr_en_memoria(url_usar)
    identificador, data_extra = extend_jwt.obtener_informacion_token()


    body_limpio["id_usuario"]=data_extra["id_usuario"]
    error, respuesta = repo.crear_reserva(body_limpio, registro, qr_id)
    if error:
        return respuesta


    error, result = extend_email.send_reserva(qr_id, url_cancelar, qr_buffer, identificador, registro)
    if error:
        return respuesta    
 
    return jsonify({"message": "Reserva registrada, revise su bandeja de entrada"}), 201

@reserva_bp.route('/reserva/<string:qr_id>/cancelar', methods=['PUT'])
def cancelar_reserva(qr_id:str):
    return "cancelacion realizada", 204

@reserva_bp.route('/reserva/<string:qr_id>/usar', methods=['PUT'])
def usar_reserva(qr_id:str):
    return "uso realizado", 204