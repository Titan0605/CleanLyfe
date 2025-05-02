from flask import Flask, jsonify, session, Blueprint, request
from app.services.transportCalculus import Transport_fp_calculator
from app.services.electric_devices_calculator import Electric_devices_calculator
from app.models.electric_devices_model import Electric_devices_model

bp = Blueprint("carbonfp_routes", __name__)

transCal = Transport_fp_calculator()
elect_devices_model = Electric_devices_model()
devicesCal = Electric_devices_calculator()

@bp.route('/carbonfp/transport-data', methods=["POST"])
def carbonfp_transport_data():
    # Gets the response
    response = request.get_json()
    # Gets each data individualy
    distance = response.get('distance_traveled')
    consumed_fuel = response.get('consumed_fuel')
    vehicule_old = response.get('vehicule_old')
    cylinders_count = response.get('cylinders_count')
    fuel_type = response.get('fuel_type')
    
    print(f"Received data: distance={distance}, consumed_fuel={consumed_fuel}, vehicle_old={vehicule_old}, cylinders_count={cylinders_count}, fuel_type={fuel_type}")
    # # Check for missing or invalid data
    # if not distance or not consumed_fuel or not cylinders_count or not fuel_type or not vehicle_old:
    #     return jsonify({"error": "Invalid or missing data"}), 400
    
    # Calculates the emission
    result = transCal.calculate_transport_emission(int(distance), int(consumed_fuel), 0.10, 0.10, 2.31) # this will be changed with the real information
    
    print("Final emission: ", result)
    return jsonify(result)

@bp.route('/carbonfp/get-devices')
def carbonfp_get_devices():
    # Calls model to get all devices
    response = elect_devices_model.getAllDevices()
    return jsonify(response)

@bp.route('/carbonfp/get-device-id/<int:id>')
def carbonfp_get_devices_id(id):
    # Calls model to get the devices by id
    response = elect_devices_model.getDeviceById(id)
    
    return jsonify(response)

@bp.route('/carbonfp/get-device-name/<string:name>')
def carbonfp_get_device_name(name):
    # calls model to get devices by name
    response = elect_devices_model.getDeviceByName(name)
    
    return jsonify(response)

@bp.route('/carbonfp/get-device-location/<string:location>')
def carbonfp_get_device_location(location):
    # Calls model to get devices by location
    response = elect_devices_model.getDeviceByLocation(location)
    
    return jsonify(response)

@bp.route('/carbonfp/get-devices-name-selected', methods=['POST'])
def getdevices():
    try:
        response = request.get_json()    
        
        data = []
        
        for id in response['device']:        
            device = elect_devices_model.getDeviceIdNameById(id)
            data.append(device)
            
        print(data)

        return jsonify({"Status": "Devices collected successfully.", "devices": data}), 201
        
    except KeyError as error:
        return jsonify({"Status": error})


@bp.route('/carbonfp/devices/calculation-basic', methods=['POST'])
def carbonfp_basic():
    try:
        response = request.get_json()
        type_calculation = str(response['type_calculation'])
        electricity_consumption = float(response['electricity_consumption'])

        status = devicesCal.calculation_type(type_calculation, electricity_consumption, response)
        
        return jsonify({'Status': status})
    except KeyError as error:
        return jsonify({'Status': error})


@bp.route('/carbonfp/devices/calculation-accurate', methods=['POST'])
def carbonfp_accurate():
    try:
        response = request.get_json()
        electricity_consumption = response['electricity_consumption']
        type_calculation = response['type_calculation'][0]
    
        status = devicesCal.calculation_type(type_calculation, electricity_consumption, response)
        
        return jsonify({'Status': status})
    except KeyError as error:
        return jsonify({'Status': error})