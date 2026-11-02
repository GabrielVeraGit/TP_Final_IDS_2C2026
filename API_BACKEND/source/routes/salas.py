from flask import Blueprint, jsonify

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas/<id_sede>', methods=['GET'])
def get_salas_sede():
    return jsonify({"registros":"salas de una sede"}), 200

@sala_bp.route('/salas', methods=['GET'])
def get_salas():
    return jsonify({"registros":"salas"}), 200

@sala_bp.route('/salas/<id>', methods=['GET'])
def get_sala_id(id:str):
    return jsonify({"registro":"sala"}), 200

@sala_bp.route('/salas', methods=['POST'])
def post_sala():
    return jsonify({"exito":"registrado"}), 200

@sala_bp.route('/salas/<id>', methods=['PUT'])
def put_sala(id:str):
    return jsonify({"exito":"modificado"}), 200

@sala_bp.route('/salas/<id>', methods=['DELETE'])
def delete_sala(id:str):
    return jsonify({"exito":"eliminado"}), 200