
from flask import jsonify, Blueprint, request
from app.services.carbon import TransportCalculator, ElectricDevicesCalculator, WaterEmissionCalculator
from app.services.carbon.products_calculations import calculate_products_total
from app.models.carbon_energy_model import ElectricDevicesModel
from app.models.carbon_products_model import CarbonProductsModel

bp = Blueprint("carbonfp_routes", __name__)

energy_model = ElectricDevicesModel()
products_model = CarbonProductsModel()

transCal = TransportCalculator()
energyCal = ElectricDevicesCalculator()
water_emission_calc = WaterEmissionCalculator()

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
        
        print("Final transport calculations: ", result)
        carbon_footprint["transport"] = result
        return jsonify(result)
    except Exception as error:
        return jsonify({"status": "error", "msg": error})

@bp.route('/carbonfp/get-devices-name-selected', methods=['POST'])
def getdevices():
    try:
        response = request.get_json()  
        
        print(response['device'])
       
        devices = energy_model.get_devices_by_ids(response['device'])
            
        print(devices)

        return jsonify({"Status": "Devices collected successfully.", "devices": devices}), 201
        
    except KeyError as error:
        return jsonify({"Status": str(error)})


@bp.route('/carbonfp/devices/calculation-basic', methods=['POST'])
def carbonfp_basic():
    try:
        response = request.get_json()
        electricity_consumption = float(response['electricity_consumption'])

        result = energyCal.basic_calculation(electricity_consumption)
        
        carbon_footprint["energy"] = result
        
        print(carbon_footprint)
        
        if result:
            return jsonify({
                'Status': 'Energy calculated successfully.',
                'total_emission': result["totalEmission"],
                'message': f'Total weekly carbon emission: {result["totalEmission"]} kgCO2e'
            })
        else:
            return jsonify({
                'Status': 'Something went wrong, try again later.',
                'message': 'Failed to calculate emissions'
            })
    except KeyError as error:
        print(f'Error in carbonfp_basic: {error}')
        return jsonify({'Status': str(error)})

@bp.route('/carbonfp/devices/calculation-accurate', methods=['POST'])
def carbonfp_accurate():
    try:
        response = request.get_json()
        # type_calculation = response['type_calculation'][0]
        
        # Call the calculation function
        result = energyCal.accurate_calculation(response)
        
        energy_data = energy_model.calculate_energy_footprint(result)
        
        print("Final transport calculations: ", energy_data)
        carbon_footprint["energy"] = energy_data
        
        print(carbon_footprint)
        
        if energy_data:
            return jsonify({
                'Status': 'Energy calculated successfully.',
                'total_emission': energy_data["totalEmission"],
                'message': f'Total weekly carbon emission: {energy_data["totalEmission"]} kgCO2e'
            })
        else:
            return jsonify({
                'Status': 'Something went wrong, try again later.',
                'message': 'Failed to calculate emissions'
            })
            
    except Exception as error:
        print(f'Error in carbonfp_accurate: {error}')
        return jsonify({'Status': str(error)})


@bp.route('/carbonfp/products/get-products-selected', methods=['POST'])
def carbonfp_get_products():
    try:
        response = request.get_json()
    
        if response:
            return jsonify({'Status': 'Valid response.'})
        else:
            return jsonify({'Status': 'You must choose at least one.'})
       
    except Exception as error:
        return jsonify({'Status': error})



@bp.route('/carbonfp/products/get-products-info', methods=['POST'])
def carbonfp_get_products_info():
    try:
        response = request.get_json()
        # Espera un array de productos con sus datos
        # Ejemplo: [{product_type, quantity, transport, packaging, refrigeration, product_id}]
        if not response or not isinstance(response, dict):
            return jsonify({'Status': 'Invalid input.'})

        # Si el form solo manda un producto, lo convertimos a lista
        products = response.get('products')
        if not products:
            # Si el form no manda 'products', intentamos armarlo de los campos planos
            products = [response]

        # Calcula emisiones
        result = calculate_products_total(products)
        # Guarda en la base de datos
        db_result = products_model.calculate_products_footprint(result['productsEmissions'], result['totalEmission'])
        carbon_footprint['products'] = db_result
        
        print(carbon_footprint)

        return jsonify({'Status': 'Products calculation successfully.', 'result': db_result})
    except Exception as error:
        print(f'Error in carbonfp_get_products_info: {error}')
        return jsonify({'Status': str(error)})
    
@bp.route('/carbonfp/water/calculate', methods=['POST'])
def carbonfp_calculate_water():
    try:
        data = request.get_json()
        
        print(data)
        result = water_emission_calc.calculate_water_emission(
            liters=data['water_consumed'],
            heating_percentage=data['water_heated_percentage'],
            heating_type=data['heater_type']
            )
        print(result)
        
        carbon_footprint['water'] = result
        
        print(carbon_footprint)
        
        return jsonify({
            'Status': 'Water calculation successfully.',
            'waterEmission': result['totalEmission'],
            'message': f'Total water emission: {result["totalEmission"]} kgCO2e'
        })
    
    except Exception as error:
        return jsonify({'Status': 'Water calculation Failed.', 'Result': error})