from flask import Blueprint, request, jsonify
from app.models import model_waterflow

bp = Blueprint('waterflow', __name__, url_prefix='/waterflow')

@bp.route('/generate-token', methods=['POST', 'GET'])
def generate_token():
    data = request.get_json() or {}
    user_id = data.get('user_id', '').strip()
    if not user_id:
        return jsonify({"status": "error", "message": "Missing 'user_id' field"}), 400

    try:
        token = model_waterflow.generate_token_to_user(user_id)
        if not token:
            raise ValueError
        return jsonify({
        "status": "success",
        "message": "Token generated successfully",
        "user_id": user_id,
        "token": token
        }), 201
    except Exception:
        return jsonify({"status": "error", "message": "User not found or update failed"}), 404


@bp.route('/send-command', methods=['POST'])
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


@bp.route('/waterflow-state', methods=['GET'])
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
        "activate": state.get('active', False)
    }), 200


@bp.route('/send-token', methods=['POST'])
def pair_device():
    data = request.get_json() or {}
    token = data.get('token', '').strip()
    mac = data.get('waterflow_mac', '').strip()
    
    print(data)

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


@bp.route('/in-database', methods=['GET'])
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

@bp.route('/history-state', methods=['GET'])
def get_history():
    mac = request.args.get('waterflow_mac', '').strip()
    if not mac:
        return jsonify({"status": "error", "message": "Missing 'waterflow_mac' parameter"}), 400

    history = model_waterflow.get_history_of_the_waterflow(mac)
    if history is None:
        return jsonify({"status": "error", "message": "WaterFlow not found"}), 404

    return jsonify({
        "status": "success",
        "message": "History retrieved successfully",
        "waterflow_mac": mac,
        "history": history
    }), 200


@bp.route('/info-waterflow/<string:user_id>', methods=['POST'])
def get_user_waterflows_info(user_id):    
    if not user_id:
        return jsonify({"status": "error", "message": "Missing 'user_id' parameter"}), 400

    info = model_waterflow.get_information_waterflows(user_id)
    if info is None:
        return jsonify({"status": "error", "message": "No WaterFlows found for this user"}), 404

    return jsonify({
        "status": "success",
        "message": "WaterFlow information retrieved successfully",
        "waterflows": info
    }), 200

@bp.route('/get-temperature-waterflow', methods=["GET"])
def get_temperature_waterflow():
    mac_address = request.args.get("mac_address", "")
    if not mac_address:
        return jsonify({
            "status": "error",
            "message": "No mac_address sent"
        }), 400
    
    response = model_waterflow.get_temperature_waterflow(mac_address)

    if not response:
        return jsonify({
            "status": "error",
            "message": "Waterflow not found"
        }), 404
    
    return jsonify({
        "status": "successfuly",
        "message": "Information collected succesfuly",
        "results": response
    }), 200

@bp.route("/get-history-temp",methods=["GET"])
def get_history_temp():
    mac_address = request.args.get("mac_address", "")
    if not mac_address:
        return jsonify({
            "status": "error",
            "message": "No mac_address sent"
        }), 400
    
    response = model_waterflow.get_history_temp(mac_address)
    if not response:
        return jsonify({
            "status": "error",
            "message": "Waterflow not found"
        }), 404
    
    return jsonify({
        "status": "successfuly",
        "message": "Information collected succesfuly",
        "results": response
    }), 200

@bp.route("/send-temperature", methods=["POST"])
def send_temperature():
    data = request.get_json()
    if not data or not "mac_address" in data or not "temp" in data:
        return jsonify({
            "status": "error",
            "message": "no data sent"
        }), 400
    
    mac_address = data.get("mac_address", "")
    temp = data.get("temp", "")

    response = model_waterflow.send_temp(mac_address, temp)

    if not response:
        return jsonify({
            "status": "error",
            "message": "something went wrong with the update"
        })
    
    return jsonify({
        "status": "successfuly",
        "message": "the update went well"
    }), 200

@bp.route("/set-configuration", methods=["PUT"])
def set_configuration():
    data = request.get_json()
    if not data or not "autoCloseTemp" in data or "autoClose" not in data or "name" not in data:
        return jsonify({
            "status": "error",
            "message": "missing json or missing fields"
        }), 400
    
    mac_address = data.get("mac_address", "")
    autoCloseTemp = data.get("autoCloseTemp", 0)
    autoClose = data.get("autoClose", False)
    name = data.get("name", "New waterflow")

    success = model_waterflow.modify_waterflow_settings(mac_address, autoCloseTemp, autoClose, name)

    if not success:
        return jsonify({
            "status": "error",
            "message": "the update was not successful"
        }), 400
    
    return jsonify({
        "status": "successfuly",
        "message": "the update went well"
    }), 200

@bp.route("/get-notifications", methods=["GET"])
def get_notifications():
    user_id = request.args.get("user_id", "")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "no user id sent"
        }), 400
    
    notifications = model_waterflow.get_notifications(user_id)

    if not notifications:
        return jsonify({
            "status": "error",
            "message": "Something went wrong"
        }), 404
    
    return jsonify({
        "status": "successfuly",
        "message": "notifications was gotten well",
        "notifications": notifications
    }), 200

@bp.route("/get-configuration",methods=["GET"])
def get_configuration():
    mac_address = request.args.get("mac_address", "")
    if not mac_address:
        return jsonify({
            "status": "error",
            "message": "No mac_address sent"
        }), 400
    
    response = model_waterflow.get_configuration(mac_address)
    if not response:
        return jsonify({
            "status": "error",
            "message": "Waterflow not found"
        }), 404
    
    return jsonify({
        "status": "successfuly",
        "message": "Information collected succesfuly",
        "results": response
    }), 200