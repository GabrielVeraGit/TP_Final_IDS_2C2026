from errors_code import ERROR_CLIENTE
from vars_validacion import DOMINIOS_MAIL_PERMITIDOS
from source.repositories.users import obtener_emails_admins, obtener_usuarios_filtros
from email_validator import validate_email, EmailNotValidError

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


def buscar_rol_email(usr:dict):
    email=usr["email"]
    error, resultado =obtener_emails_admins()
    if error:
        return True, resultado
    
    tipo_rol="cliente"
    if email in resultado:
        tipo_rol="admin"

    return False, tipo_rol

def verificar_unicidad_email_usuarios(usr:dict):
    error, resultado = obtener_usuarios_filtros({"email":usr["email"]})
    if error:
        return True, resultado
    
    if len(resultado)==0:
        return False, None
    return True, ERROR_CLIENTE["CONFLICT"]("El email ya existe en DB")
