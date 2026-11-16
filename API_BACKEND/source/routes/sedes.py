from flask import Blueprint, jsonify


from source import extend_jwt
from source.validators import sedes as val
from source.services import sedes as serv

sede_bp = Blueprint('sede', __name__)

@sede_bp.route('/sedes', methods=['GET'])
@extend_jwt.seguro()
def get_sedes():
    error, registros = serv.listar_sedes()
    if error:
        return registros
    return jsonify(registros), 200

@sede_bp.route('/sedes/<int:id_sede>', methods=['GET'])
@extend_jwt.seguro()
def get_sede_id(id_sede:int):
    error, registro = serv.obtener_sede(id_sede)
    if error:
        return registro
    return jsonify(registro), 200

@sede_bp.route('/sedes', methods=['POST'])
@extend_jwt.seguro()
def post_sede():
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
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
@extend_jwt.seguro()
def put_sede(id_sede:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
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
@extend_jwt.seguro()
def delete_sede(id_sede:int):
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, resultado = serv.eliminar_sede(id_sede)
    if error:
        return resultado
    return jsonify({"message": "Sede eliminada"}), 200