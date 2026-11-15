from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required 

from source import extend_jwt
from source.validators import sedes as val
from source.services import sedes as serv
from source.services import users as serv_users

sede_bp = Blueprint('sede', __name__)

@sede_bp.route('/sedes', methods=['GET'])
@jwt_required()
def get_sedes():
    error, registros = serv.listar_sedes()
    if error:
        return registros
    return jsonify(registros), 200

@sede_bp.route('/sedes/<int:id_sede>', methods=['GET'])
@jwt_required()
def get_sede_id(id_sede:int):
    error, registro = serv.obtener_sede(id_sede)
    if error:
        return registro
    return jsonify(registro), 200

@sede_bp.route('/sedes', methods=['POST'])
@jwt_required()
def post_sede():
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv_users.verificar_rol_permitido(data_extra, "admin")
    if error:
        return resultado
    error, datos = val.validar_campos_sede()
    if error:
        return datos
    error, id_sede = serv.crear_sede(datos)
    if error:
        return id_sede
    return jsonify({"message": "Sede registrada", "id_sede": id_sede}), 201

@sede_bp.route('/sedes/<int:id_sede>', methods=['PUT'])
@jwt_required()
def put_sede(id_sede:int):
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv_users.verificar_rol_permitido(data_extra, "admin")
    if error:
        return resultado
    error, datos = val.validar_campos_sede()
    if error:
        return datos
    error, resultado = serv.modificar_sede(id_sede, datos)
    if error:
        return resultado
    return jsonify({"message": "Sede modificada"}), 200

@sede_bp.route('/sedes/<int:id_sede>', methods=['DELETE'])
@jwt_required()
def delete_sede(id_sede:int):
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv_users.verificar_rol_permitido(data_extra, "admin")
    if error:
        return resultado
    error, resultado = serv.eliminar_sede(id_sede)
    if error:
        return resultado
    return jsonify({"message": "Sede eliminada"}), 200