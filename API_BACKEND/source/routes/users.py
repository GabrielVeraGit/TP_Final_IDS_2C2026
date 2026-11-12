from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from sends_mails import send_email

from source.auth import requiere_login, requiere_admin, obtener_token
from source.validators.users import validando_campos_registro, validar_login
from source.services.users import buscar_rol_email, verificar_unicidad_email_usuarios, validando_dominio_email
from source.services.users import iniciar_sesion, cerrar_sesion, obtener_perfil, listar_usuarios
from source.repositories.users import append_usuarios

user_bp = Blueprint('user', __name__)

#informacion por request body

@user_bp.route('/user', methods=['GET'])
@requiere_login
def get_user(usuario):
    return jsonify(usuario), 200

@user_bp.route('/user/perfil', methods=['GET'])
@requiere_login
def get_perfil(usuario):
    error, resultado = obtener_perfil(usuario)
    if error:
        return resultado
    return jsonify(resultado), 200

@user_bp.route('/user/register', methods=['POST'])
def register_user():
    error, data = validando_campos_registro()
    if error: 
        return data
    error, resultado = validando_dominio_email(data)
    if error:
        return resultado
    error, resultado = verificar_unicidad_email_usuarios(data)
    if error:
        return resultado
    
    error, resultado = buscar_rol_email(data)
    if error:
        return resultado

    data["password"]=generate_password_hash(data["password"])
    data["rol"]=resultado

    error, resultado = send_email("Este es un asunto, BIEMBENIDO",[data["email"]], "este es el cuerpo")
    if error:
        return resultado
    
    error, resultado = append_usuarios(data)
    if error:
        return resultado

    return jsonify({"message": "Usuario registrado, revise su bandeja de entrada"}), 201

@user_bp.route('/user/login', methods=['POST'])
def login_user():
    error, datos = validar_login(request.get_json(silent=True))
    if error:
        return datos
    error, resultado = iniciar_sesion(datos["email"], datos["password"])
    if error:
        return resultado
    resultado["message"] = "Usuario inicio sesion"
    return jsonify(resultado), 200


@user_bp.route('/user/logout', methods=['POST'])
@requiere_login
def logout_user(usuario):
    error, token = obtener_token()
    cerrar_sesion(token)
    return jsonify({"message": "Usuario cerro sesion"}), 200

#Lista usuarios a admin
@user_bp.route('/users', methods=['GET'])
@requiere_admin
def get_users():
    error, resultado = listar_usuarios()
    if error:
        return resultado
    return jsonify(resultado), 200