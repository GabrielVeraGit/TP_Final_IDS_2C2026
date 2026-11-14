from flask import jsonify
from errors_code import ERROR_CLIENTE
from source.utils.validaciones import DOMINIOS_MAIL_PERMITIDOS
from source.repositories import users as repo
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

def validando_dominio_email(usr:dict):
    correo=usr["email"]
    try:
        correo_val = validate_email(correo, check_deliverability=True)
        if correo_val.domain not in DOMINIOS_MAIL_PERMITIDOS:
            return True, ERROR_CLIENTE["UNPROCESSABLE_ENTITY"](f"Dominio de correo no permitido, se permiten: {DOMINIOS_MAIL_PERMITIDOS}")
        usr["email"] = str(correo_val.email.lower())
        return False, None

    except EmailNotValidError as e:
        return True, ERROR_CLIENTE["BAD_REQUEST"](f"Direccion de correo no valida, motivo: {str(e)}")

def buscar_rol_registro(usr:dict):
    email=usr["email"]
    error, resultado = repo.obtener_emails_admins()
    if error:
        return True, resultado
    
    tipo_rol="cliente"
    if email in resultado:
        tipo_rol="admin"

    return False, tipo_rol

def verificar_unicidad_email_usuarios(usr:dict):
    error, resultado = repo.obtener_usuarios_filtros({"email":usr["email"]})
    if error:
        return True, resultado
    
    if len(resultado)==0:
        return False, None
    return True, ERROR_CLIENTE["CONFLICT"]("El email ya existe en DB")


def encriptar_password(password):
    password_encriptada = generate_password_hash(password)
    return password_encriptada
def verificar_igualdad_password(hash_password:str, password:str):
    if check_password_hash(hash_password, password):
        return False, None
    return True, ERROR_CLIENTE["UNAUTHORIZED"]("contrasenia incorrecta")

def verificar_rol_permitido(data_extra:dict, rol_permitido:str):
    if data_extra["rol"] == rol_permitido:
        return False, None
    return True, ERROR_CLIENTE["FORBIDDEN"](f"Usted no es {rol_permitido}")


def obtener_perfil(identificador:str):
    error, registro = repo.obtener_usuarios_filtros({"email":identificador})
    if error:
        return True, registro
    usuario=registro[0]
    resultado = {
        "usuario": usuario,
        "consumos": repo.obtener_resumen_consumos(usuario["id_usuario"]),
        "peliculas_vistas": repo.obtener_peliculas_vistas(usuario["id_usuario"]),
    }
    return False, resultado

def listar_usuarios():
    error, registros = repo.obtener_usuarios_filtros(con_password=False)
    if error:
        return True, registros
    return False, registros


def obtener_usuario_login(usr:dict):
    error, resultado = repo.obtener_usuarios_filtros({"email":usr["email"]}, con_password=True)
    if error:
        return True, resultado
    
    if len(resultado)==0:
        return True, ERROR_CLIENTE["NOT_FOUND"]("El email no esta registrado")
    return False, resultado[0]