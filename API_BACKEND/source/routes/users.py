from flask import Blueprint, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sends_mails import send_email

from source.validators.users import validando_campos_registro
from source.services.users import buscar_rol_email, verificar_unicidad_email_usuarios, validando_dominio_email
from source.repositories.users import append_usuarios
user_bp = Blueprint('user', __name__)

#informacion por request body

@user_bp.route('/user', methods=['GET'])
def get_user():
    return jsonify({"mensaje": "usuario obtenido"}), 200

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
    return jsonify({"mensaje": "usuario inicio sesion"}), 200

@user_bp.route('/user/logout', methods=['POST'])
def logout_user():
    return jsonify({"mensaje": "usuario cerro sesion"}), 200