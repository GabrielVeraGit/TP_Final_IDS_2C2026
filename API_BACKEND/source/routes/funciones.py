from flask import Blueprint, jsonify
from source import extend_jwt
from source.validators import funciones as val
from source.services import funciones as serv


funcion_bp = Blueprint('funcion', __name__)

@funcion_bp.route('/funciones', methods=['GET'])
@extend_jwt.seguro()
def get_funciones():
    error, filtros = val.validar_filtros_funciones()
    if error:
        return filtros
    error, registros = serv.listar_funciones(filtros)
    if error:
        return registros
    return jsonify(registros), 200


@funcion_bp.route('/funciones/<int:id_funcion>', methods=['GET'])
@extend_jwt.seguro()
def get_funcion_id(id_funcion:int):
    error, registro = serv.obtener_funcion(id_funcion)
    if error:
        return registro
    return jsonify(registro), 200

@funcion_bp.route('/funciones', methods=['POST'])
@extend_jwt.seguro()
def post_funcion():
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_campos_funcion()
    if error:
        return datos
    error, id_funcion = serv.crear_funcion(datos)
    if error:
        return id_funcion
    return jsonify({"message": "Funcion registrada", "id_funcion": id_funcion}), 201


@funcion_bp.route('/funciones/<int:id_funcion>', methods=['PUT'])
@extend_jwt.seguro()
def put_funcion(id_funcion:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_campos_funcion()
    if error:
        return datos
    error, resultado = serv.modificar_funcion(id_funcion, datos)
    if error:
        return resultado
    return jsonify({"message": "Funcion modificada"}), 200

@funcion_bp.route('/funciones/<int:id_funcion>', methods=['DELETE'])
@extend_jwt.seguro()
def delete_funcion(id_funcion:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, resultado = serv.eliminar_funcion(id_funcion)
    if error:
        return resultado
    return jsonify({"message": "Funcion eliminada"}), 200