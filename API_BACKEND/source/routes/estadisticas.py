from flask import Blueprint, jsonify
from source import extend_jwt
from source.services import estadisticas as serv

estadistica_bp = Blueprint("estadistica", __name__)


@estadistica_bp.route("/admin/estadisticas/ocupacion", methods=["GET"])
@extend_jwt.seguro()
def get_ocupacion_funciones():
    error, respuesta = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return respuesta

    error, registros = serv.obtener_ocupacion_funciones()
    if error:
        return registros

    return jsonify({"registros": registros}), 200


@estadistica_bp.route("/admin/estadisticas/ventas-genero", methods=["GET"])
@extend_jwt.seguro()
def get_ventas_por_genero():
    error, respuesta = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return respuesta

    error, registros = serv.obtener_ventas_por_genero()
    if error:
        return registros

    return jsonify({"registros": registros}), 200
