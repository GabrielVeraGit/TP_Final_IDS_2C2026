from flask import Blueprint, jsonify

from source.extend_email import send_email
from source.validators import users as val
from source.services import users as serv
from source.repositories import users as repo

from source import extend_jwt
from flask_jwt_extended import jwt_required #tokens

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/register', methods=['POST'])
def register_user():
    error, data = val.validando_campos_registro()
    if error: 
        return data
    error, resultado = serv.validando_dominio_email(data)
    if error:
        return resultado
    error, resultado = serv.verificar_unicidad_email_usuarios(data)
    if error:
        return resultado
    
    error, resultado = serv.buscar_rol_registro(data)
    if error:
        return resultado

    data["password"] = serv.encriptar_password(data["password"])
    data["rol"]=resultado

    error, resultado = repo.append_usuarios(data)
    if error:
        return resultado
    
    error, resultado = send_email("Este es un asunto, BIEMBENIDO",[data["email"]], "este es el cuerpo")
    if error:
        return resultado
    
    return jsonify({"message": "Usuario registrado, revise su bandeja de entrada"}), 201

@user_bp.route('/user/login', methods=['POST'])
def login_user():
    error, datos = val.validar_login()
    if error:
        return datos
  
    error, registro = serv.obtener_usuario_login(datos)
    if error:
        return registro
 
    error, resultado = serv.verificar_igualdad_password(registro["password"], datos["password"])
    if error:
        return resultado
    #hasta aca, credenciales correctas, y el registo del usuario
    
    token = extend_jwt.crear_token(registro)
    respuesta = extend_jwt.crear_cookie(token)
    return respuesta, 201

@user_bp.route('/user/logout', methods=['POST'])
@jwt_required()
def logout_user():
    respuesta = extend_jwt.eliminar_cookie()
    return respuesta, 201

@user_bp.route('/user/perfil', methods=['GET'])#para clientes
@jwt_required()
def get_perfil():
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv.verificar_rol_permitido(data_extra, "cliente")
    if error:
        return resultado
    error, resultado = serv.obtener_perfil(identificador)
    if error:
        return resultado
    return jsonify(resultado), 200

@user_bp.route('/users', methods=['GET'])#Lista usuarios a admin
@jwt_required()
def get_users():
    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv.verificar_rol_permitido(data_extra, "admin")
    if error:
        return resultado
    error, registros = serv.listar_usuarios()
    if error:
        return registros
    return jsonify(registros), 200