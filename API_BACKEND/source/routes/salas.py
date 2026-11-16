from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required 

from source import extend_jwt
from source.validators import salas as val
from source.services import salas as serv
from source.services import users as serv_users

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['GET'])
@jwt_required()
def get_salas():
    error, filtros = val.validar_filtros_salas()
    if error:
        return filtros
    error, registros = serv.listar_salas(filtros["id_sede"])
    if error:
        return registros
    return jsonify(registros), 200

@sala_bp.route('/salas/<int:id_sala>', methods=['GET'])
@jwt_required()
def get_sala_id(id_sala:int):
    error, registro = serv.obtener_sala(id_sala)
    if error:
        return registro
    return jsonify(registro), 200

@sala_bp.route('/salas', methods=['POST'])
@jwt_required()
def post_sala():
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv_users.verificar_rol_permitido(data_extra, "admin")
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
@jwt_required()
def put_sala(id_sala:int):
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv_users.verificar_rol_permitido(data_extra, "admin")
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
@jwt_required()
def delete_sala(id_sala:int):
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv_users.verificar_rol_permitido(data_extra, "admin")
    if error:
        return resultado
    error, resultado = serv.eliminar_sala(id_sala)
    if error:
        return resultado
    return jsonify({"message": "Sala eliminada"}), 200