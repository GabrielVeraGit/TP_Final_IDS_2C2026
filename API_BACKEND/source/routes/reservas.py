from flask import Blueprint, jsonify

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/reservas', methods=['GET'])
def get_reservas():
    return jsonify({"registros":"reservas"}), 200

@reserva_bp.route('/reservas/<id_reserva>', methods=['GET'])
def get_reserva(id_reserva:str):
    return jsonify({"registros":"reserva"}), 200

@reserva_bp.route('/reservas', methods=['POST'])
def create_reserva():
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