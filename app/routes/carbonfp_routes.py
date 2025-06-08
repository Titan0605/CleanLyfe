from flask import jsonify, Blueprint, request
from app.services.carbon.transport_calculations import TransportCalculator
# from app.services.electric_devices_calculator import Electric_devices_calculator
# from app.services.carbon_water_calculus import WaterEmissionCalculator
# from app.models.electric_devices_model import Electric_devices_model

bp = Blueprint("carbonfp_routes", __name__)

transCal = TransportCalculator()
# elect_devices_model = Electric_devices_model()
# devicesCal = Electric_devices_calculator()
# water_emission_calc = WaterEmissionCalculator()

carbon_footprint = {}

@bp.route('/carbonfp/transport-data', methods=["POST"])
def carbonfp_transport_data():
    # Gets the response
    try:
        response = request.get_json()
        data = dict(response)
        
        # Calculates the emission
        result = transCal.calculate_transport_footprint(
    int(data["distance_traveled"]),
    int(data["consumed_fuel"]),
    int(data["vehicule_old"]),
    int(data["cylinders_count"]),
    data["fuel_type"]
        )
        
        print("Final calculations: ", result)
        carbon_footprint["transport"] = result
        return jsonify(result)
    except Exception as error:
        return jsonify({"status": "error", "msg": error})

# @bp.route('/carbonfp/get-devices')
# def carbonfp_get_devices():
#     # Calls model to get all devices
#     response = elect_devices_model.getAllDevices()
#     return jsonify(response)

# @bp.route('/carbonfp/get-device-id/<int:id>')
# def carbonfp_get_devices_id(id):
#     # Calls model to get the devices by id
#     response = elect_devices_model.getDeviceById(id)
    
#     return jsonify(response)

# @bp.route('/carbonfp/get-device-name/<string:name>')
# def carbonfp_get_device_name(name):
#     # calls model to get devices by name
#     response = elect_devices_model.getDeviceByName(name)
    
#     return jsonify(response)

# @bp.route('/carbonfp/get-device-location/<string:location>')
# def carbonfp_get_device_location(location):
#     # Calls model to get devices by location
#     response = elect_devices_model.getDeviceByLocation(location)
    
#     return jsonify(response)

# @bp.route('/carbonfp/get-devices-name-selected', methods=['POST'])
# def getdevices():
#     try:
#         response = request.get_json()    
        
#         data = []
        
#         for id in response['device']:        
#             device = elect_devices_model.getDeviceIdNameById(id)
#             data.append(device)
            
#         print(data)

#         return jsonify({"Status": "Devices collected successfully.", "devices": data}), 201
        
#     except KeyError as error:
#         return jsonify({"Status": error})


# @bp.route('/carbonfp/devices/calculation-basic', methods=['POST'])
# def carbonfp_basic():
#     try:
#         response = request.get_json()
#         type_calculation = str(response['type_calculation'])
#         electricity_consumption = float(response['electricity_consumption'])

#         status = devicesCal.calculation_type(type_calculation, electricity_consumption, response)
        
#         if status == 'Electric calculation successfully.':
#             status = 'Carbonfp successfully.'
#         elif status == 'Failed electrical calculation.':
#             status = 'Something went wrong, try again later.'
        
#         return jsonify({'Status': status})
#     except KeyError as error:
#         return jsonify({'Status': error})


# @bp.route('/carbonfp/devices/calculation-accurate', methods=['POST'])
# def carbonfp_accurate():
#     try:
#         response = request.get_json()
#         electricity_consumption = response['electricity_consumption']
#         type_calculation = response['type_calculation'][0]
    
#         status = devicesCal.calculation_type(type_calculation, electricity_consumption, response)
        
#         if status == 'Electric calculation successfully.':
#             status = 'Carbonfp successfully.'
#         elif status == 'Failed electrical calculation.':
#             status = 'Something went wrong, try again later.'
        
#         return jsonify({'Status': status})
#     except KeyError as error:
#         return jsonify({'Status': error})


# @bp.route('/carbonfp/products/get-products-selected', methods=['POST'])
# def carbonfp_get_products():
#     try:
#         response = request.get_json()
        
#         if response:
#             return jsonify({'Status': 'Valid response.'})
#         else:
#             return jsonify({'Status': 'You must choose at least one.'})
            
#     except Exception as error:
#         return jsonify({'Status': error})


# @bp.route('/carbonfp/products/get-products-info', methods=['POST'])
# def carbonfp_get_products_info():
#     try:
#         response = request.get_json()
        
#         print(f'response: {response}')
        
#         return jsonify({'Status': 'Products calculation successfully.'})
#     except Exception as error:
#         return jsonify({'Status': error})
    
# @bp.route('/carbonfp/water/calculate', methods=['POST'])
# def carbonfp_calculate_water():
#     try:
#         data = request.get_json()
        
#         print(data)
#         emission = water_emission_calc.calculate_water_emission(
#             liters=data['water_consumed'],
#             heating_percentage=data['water_heated_percentage'],
#             heating_type=data['heater_type']
#             )
#         print(emission)
        
#         return jsonify({'Status': 'Response recieved', 'Result': emission})
    
#     except Exception as error:
#         return jsonify({'Status:', error})