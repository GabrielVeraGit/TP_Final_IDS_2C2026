from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

#informacion por request body

@user_bp.route('/user', methods=['GET'])
def get_user():
    return jsonify({"mensaje": "usuario obtenido"}), 200

@user_bp.route('/user/register', methods=['POST'])
def register_user():
    return jsonify({"mensaje": "usuario registrado"}), 200

@user_bp.route('/user/login', methods=['POST'])
def login_user():
    return jsonify({"mensaje": "usuario inicio sesion"}), 200

@user_bp.route('/user/logout', methods=['POST'])
def logout_user():
    return jsonify({"mensaje": "usuario cerro sesion"}), 200