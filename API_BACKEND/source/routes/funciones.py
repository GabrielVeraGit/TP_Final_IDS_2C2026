from flask import Blueprint, jsonify

funcion_bp = Blueprint('funcion', __name__)


@funcion_bp.route('/funciones', methods=['GET'])
def get_funciones():
    return jsonify({"registros":"funciones"}), 200

@funcion_bp.route('/funciones/<id_funcion>', methods=['GET'])
def get_funcion_id(id_funcion):
    return jsonify({"registro":"funcion"}), 200

@funcion_bp.route('/funciones/pelicula', methods=['GET'])#?id_pelicula=x
def get_funciones_x_pelicula():
    return jsonify({"registros":"funciones disponibles de una pelicula"}), 200

@funcion_bp.route('/funciones', methods=['POST'])
def post_funcion():
    return jsonify({"exito":"registrado"}), 200

@funcion_bp.route('/funciones/<id_funcion>', methods=['PUT'])
def put_funcion(id_funcion:str):
    return jsonify({"exito":"modificado"}), 200

@funcion_bp.route('/funciones/<id_funcion>', methods=['DELETE'])
def delete_funcion(id_funcion:str):
    return jsonify({"exito":"eliminado"}), 200
