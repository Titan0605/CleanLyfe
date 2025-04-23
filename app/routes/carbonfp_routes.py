from flask import Flask, jsonify, session, Blueprint, request
from app.services.transportCalculus import Transport_fp_calculator

bp = Blueprint("carbonfp_routes", __name__)

transCal = Transport_fp_calculator()

@bp.route('/carbonfp/transport-data', methods=["POST"])
def carbonfp_transport_data():
    # Gets the response
    response = request.get_json()
    print(response)
    # Gets each data individualy
    distance = response.get('distance_traveled')
    consumed_fuel = response.get('consumed_fuel')
    vehicule_old = response.get('vehicule_old')
    cylinders_count = response.get('cylinders_count')
    fuel_type = response.get('fuel_type')
    time_used = response.get('time_used')
    
    print(f"Received data: distance={distance}, consumed_fuel={consumed_fuel}, vehicle_old={vehicule_old}, cylinders_count={cylinders_count}, fuel_type={fuel_type}")
    # # Check for missing or invalid data
    # if not distance or not consumed_fuel or not cylinders_count or not fuel_type or not vehicle_old:
    #     return jsonify({"error": "Invalid or missing data"}), 400
    
    # Calculates the emission
    final_emission = transCal.calculate_transport_emission(int(distance), int(consumed_fuel), 0.10, 0.10, 2.31) # this will be changed with the real information
    
    print("Final emission: ", final_emission)
    return jsonify(final_emission)