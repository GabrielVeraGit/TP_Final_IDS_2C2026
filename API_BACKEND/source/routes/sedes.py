from flask import Blueprint, jsonify

sedes_bp = Blueprint('sedes', __name__)

@sedes_bp.route('/sedes', methods=['GET'])
def get_sedes():
    return jsonify({"registros":"sedes"}), 200