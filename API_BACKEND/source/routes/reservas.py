from flask import Blueprint, jsonify
from source import extend_jwt

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

@reserva_bp.route('/reservas/<id_reserva>', methods=['GET'])
def get_reserva(id_reserva:str):
    return jsonify({"registros":"reserva"}), 200

@extend_jwt.seguro()
@reserva_bp.route('/reservas', methods=['POST'])
def create_reserva():
    error, result = extend_jwt.verificar_rol_permitido("cliente")
    if error:
        return result
    
    """
    Recibe los dato, genera el registro, genera el qr y envia el mail en background, guarda el registro
    qr almecenara el endpoint de usar_reserva
    """
    return "registro creado", 201

@reserva_bp.route('/reserva/<id_reserva>/cancelacion', methods=['PUT'])
def cancelar_reserva(id_reserva:str):
    return "cancelacion realizada", 204

@reserva_bp.route('/reserva/<id_reserva>/usada', methods=['PUT'])
def usar_reserva(id_reserva:str):
    return "uso realizado", 204