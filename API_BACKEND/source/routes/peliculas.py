from flask import Blueprint, jsonify
from source import extend_jwt
from source.validators import peliculas as val
from source.services import peliculas as serv

pelicula_bp = Blueprint('pelicula', __name__)

@pelicula_bp.route('/peliculas', methods=['GET'])
@extend_jwt.seguro()
def get_peliculas():
    error, filtros = val.validar_filtros_peliculas()
    if error:
        return filtros
    error, registros = serv.listar_peliculas(filtros)
    if error:
        return registros
    return jsonify(registros), 200


@pelicula_bp.route('/peliculas/cartelera', methods=['GET'])
@extend_jwt.seguro()
def get_cartelera():
    error, filtros = val.validar_filtros_peliculas()
    if error:
        return filtros
    error, registros = serv.listar_peliculas(filtros, True)
    if error:
        return registros
    return jsonify(registros), 200


@pelicula_bp.route('/peliculas/<int:id_pelicula>', methods=['GET'])
@extend_jwt.seguro()
def get_pelicula_id(id_pelicula:int):
    error, registro = serv.obtener_pelicula(id_pelicula)
    if error:
        return registro
    return jsonify(registro), 200

@pelicula_bp.route('/peliculas', methods=['POST'])
@extend_jwt.seguro()
def post_pelicula():
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_importacion()
    if error:
        return datos
    error, id_pelicula = serv.importar_pelicula(datos)
    if error:
        return id_pelicula
    return jsonify({"message": "Pelicula importada", "id_pelicula": id_pelicula}), 201

@pelicula_bp.route('/peliculas/<int:id_pelicula>', methods=['PUT'])
@extend_jwt.seguro()
def put_pelicula(id_pelicula:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_modificacion()
    if error:
        return datos
    error, resultado = serv.modificar_disponibilidad(id_pelicula, datos)
    if error:
        return resultado
    return jsonify({"message": "Pelicula modificada"}), 200

@pelicula_bp.route('/peliculas/<int:id_pelicula>', methods=['DELETE'])
@extend_jwt.seguro()
def delete_pelicula(id_pelicula:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, resultado = serv.eliminar_pelicula(id_pelicula)
    if error:
        return resultado
    return jsonify({"message": "Pelicula eliminada"}), 200