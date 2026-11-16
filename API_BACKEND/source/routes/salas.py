from flask import Blueprint, jsonify

from source import extend_jwt
from source.validators import salas as val
from source.services import salas as serv

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['GET'])
@extend_jwt.seguro()
def get_salas():
    error, filtros = val.validar_filtros_salas()
    if error:
        return filtros
    error, registros = serv.listar_salas(filtros["id_sede"])
    if error:
        return registros
    return jsonify(registros), 200

@sala_bp.route('/salas/<int:id_sala>', methods=['GET'])
@extend_jwt.seguro()
def get_sala_id(id_sala:int):
    error, registro = serv.obtener_sala(id_sala)
    if error:
        return registro
    return jsonify(registro), 200

@sala_bp.route('/salas', methods=['POST'])
@extend_jwt.seguro()
def post_sala():
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_campos_sala()
    if error:
        return datos
    error, id_sala = serv.crear_sala(datos)
    if error:
        return id_sala
    return jsonify({"message": "Sala registrada", "id_sala": id_sala}), 201

@sala_bp.route('/salas/<int:id_sala>', methods=['PUT'])
@extend_jwt.seguro()
def put_sala(id_sala:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_campos_sala()
    if error:
        return datos
    error, resultado = serv.modificar_sala(id_sala, datos)
    if error:
        return resultado
    return jsonify({"message": "Sala modificada"}), 200

@sala_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
@extend_jwt.seguro()
def delete_sala(id_sala:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, resultado = serv.eliminar_sala(id_sala)
    if error:
        return resultado
    return jsonify({"message": "Sala eliminada"}), 200