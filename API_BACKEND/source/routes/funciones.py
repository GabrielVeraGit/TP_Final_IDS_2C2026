from flask import Blueprint, jsonify

funcion_bp = Blueprint('funcion', __name__)

@funcion_bp.route('/funciones/<id_pelicula>', methods=['GET'])
def get_pelicula_funciones(id_pelicula:str):
    return jsonify({"registros":"funciones disponibles de una pelicula"}), 200

@funcion_bp.route('/funciones', methods=['GET'])
def get_funciones():
    return jsonify({"registros":"funciones"}), 200

@funcion_bp.route('/funciones/<id>', methods=['GET'])
def get_funcion_id(id:str):
    return jsonify({"registro":"funcion"}), 200

@funcion_bp.route('/funciones', methods=['POST'])
def post_funcion():
    return jsonify({"exito":"registrado"}), 200

@funcion_bp.route('/funciones/<id>', methods=['PUT'])
def put_funcion(id:str):
    return jsonify({"exito":"modificado"}), 200

@funcion_bp.route('/funciones/<id>', methods=['DELETE'])
def delete_funcion(id:str):
    return jsonify({"exito":"eliminado"}), 200
