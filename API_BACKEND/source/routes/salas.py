from flask import Blueprint, jsonify

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['GET'])
def get_salas():
    return jsonify({"registros":"listar todas las salas"}), 200

@sala_bp.route('/salas/<id_sala>', methods=['GET'])
def get_sala_id(id_sala:str):
    return jsonify({"registro":"sala"}), 200

@sala_bp.route('/salas/sede', methods=['GET'])#?id_sede=x
def get_salas_x_sede():
    return jsonify({"registros":"salas de una sede"}), 200

@sala_bp.route('/salas', methods=['POST'])
def post_sala():
    return jsonify({"exito":"registrado"}), 200

@sala_bp.route('/salas/<id_sala>', methods=['PUT'])
def put_sala(id_sala:str):
    return jsonify({"exito":"modificado"}), 200

@sala_bp.route('/salas/<id_sala>', methods=['DELETE'])
def delete_sala(id_sala:str):
    return jsonify({"exito":"eliminado"}), 200