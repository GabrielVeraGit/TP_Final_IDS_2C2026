from flask import Blueprint, jsonify

pelicula_bp = Blueprint('pelicula', __name__)

@pelicula_bp.route('/peliculas', methods=['GET'])
def get_peliculas():
    return jsonify({"registros":"peliculas"}), 200

@pelicula_bp.route('/peliculas/<id_pelicula>', methods=['GET'])
def get_pelicula_id(id_pelicula:str):
    return jsonify({"registro":"pelicula"}), 200

@pelicula_bp.route('/peliculas', methods=['POST'])
def post_pelicula():
    return jsonify({"exito":"registrado"}), 200

@pelicula_bp.route('/peliculas/<id_pelicula>', methods=['PUT'])
def put_pelicula(id_pelicula:str):
    return jsonify({"exito":"modificado"}), 200

@pelicula_bp.route('/peliculas/<id_pelicula>', methods=['DELETE'])
def delete_pelicula(id_pelicula:str):
    return jsonify({"exito":"eliminado"}), 200