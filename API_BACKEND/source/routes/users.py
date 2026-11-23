from flask import Blueprint, jsonify

from source.validators import users as val
from source.services import users as serv
from source.repositories import users as repo

from source import extend_jwt, extend_email

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
    
    error, resultado = extend_email.send_bienvenida(data)
    if error:
        return jsonify({"message": "Usuario registrado, pero no se pudo enviar el mail de bienvenida"}), 201
    
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
    return respuesta, 200

@user_bp.route('/user/logout', methods=['POST'])
@extend_jwt.seguro()
def logout_user():
    respuesta = extend_jwt.eliminar_cookie()
    return respuesta, 200

@user_bp.route('/user/perfil', methods=['GET'])#para clientes
@extend_jwt.seguro()
def get_perfil():
    error, resultado = extend_jwt.verificar_rol_permitido("cliente")
    if error:
        return resultado

    identificador, data_extra = extend_jwt.obtener_informacion_token()
    error, resultado = serv.obtener_perfil(identificador)
    if error:
        return resultado
    return jsonify(resultado), 200

@user_bp.route('/users', methods=['GET'])#Lista usuarios a admin
@extend_jwt.seguro()
def get_users():
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    
    error, registros = serv.listar_usuarios()
    if error:
        return registros
    return jsonify({"registros":registros}), 200

@user_bp.route('/emails-admin', methods=['POST'])
@extend_jwt.seguro()
def post_email_admin():
    error, resultado = extend_jwt.verificar_rol_permitido("admin")
    if error:
        return resultado
    error, datos = val.validar_email_admin()
    if error:
        return datos
    error, resultado = serv.registrar_email_admin(datos)
    if error:
        return resultado
    return jsonify({"message": "Email registrado como admin"}), 201