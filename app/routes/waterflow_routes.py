from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from models import model_waterflow

waterflow_bp = Blueprint('waterflow', __name__, url_prefix='/waterflow')

@waterflow_bp.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.get_json() or {}
    user_id = data.get('user_id', '').strip()
    if not user_id:
        return jsonify({"status": "error", "message": "Missing 'user_id' field"}), 400

    try:
        success = model_waterflow.generate_token_to_user(user_id)
        if not success:
            raise ValueError
        return jsonify({
            "status": "success",
            "message": "Token generated successfully",
            "user_id": user_id
        }), 201
    except Exception:
        return jsonify({"status": "error", "message": "User not found or update failed"}), 404


@waterflow_bp.route('/send-command', methods=['POST'])
def send_command():
    data = request.get_json() or {}
    mac = data.get('waterflow_mac', '').strip()
    activate = data.get('activate', None)

    if not mac or not isinstance(activate, bool):
        return jsonify({
            "status": "error",
            "message": "Missing 'waterflow_mac' or invalid 'activate' boolean"
        }), 400

    try:
        success = model_waterflow.send_command_to_change(mac, activate)
        if not success:
            raise ValueError
        return jsonify({
            "status": "success",
            "message": f"WaterFlow state changed to {activate}"
        }), 200
    except Exception:
        return jsonify({"status": "error", "message": "Device not found or update failed"}), 404


@waterflow_bp.route('/state', methods=['GET'])
def get_state():
    mac = request.args.get('waterflow_mac', '').strip()
    if not mac:
        return jsonify({"status": "error", "message": "Missing 'waterflow_mac' parameter"}), 400

    state = model_waterflow.get_waterflow_state_db(mac)
    if state is None:
        return jsonify({"status": "error", "message": "WaterFlow not found"}), 404

    return jsonify({
        "status": "success",
        "message": "State retrieved successfully",
        "waterflow_mac": mac,
        "activate": state.get('activate', False)
    }), 200


@waterflow_bp.route('/pair', methods=['POST'])
def pair_device():
    data = request.get_json() or {}
    token = data.get('token', '').strip()
    mac = data.get('waterflow_mac', '').strip()

    if not token or not mac:
        return jsonify({"status": "error", "message": "Missing 'token' or 'waterflow_mac'"}), 400

    success = model_waterflow.send_token_from_waterflow(token, mac)
    if not success:
        return jsonify({"status": "error", "message": "Invalid token or pairing failed"}), 401

    return jsonify({
        "status": "success",
        "message": "WaterFlow paired successfully",
        "waterflow_mac": mac
    }), 201


@waterflow_bp.route('/exists', methods=['GET'])
def exists():
    mac = request.args.get('waterflow_mac', '').strip()
    if not mac:
        return jsonify({"status": "error", "message": "Missing 'waterflow_mac' parameter"}), 400

    exists = model_waterflow.waterflow_in_database(mac)
    return jsonify({
        "status": "success" if exists else "error",
        "is_in_database": exists,
        "message": "WaterFlow found" if exists else "WaterFlow not found"
    }), (200 if exists else 404)
