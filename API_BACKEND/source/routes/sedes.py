from flask import Blueprint, jsonify

sede_bp = Blueprint('sede', __name__)

@sede_bp.route('/sedes', methods=['GET'])
def get_sedes():
    return jsonify({"registros":"sedes"}), 200