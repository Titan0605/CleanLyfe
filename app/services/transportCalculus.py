from flask import jsonify
class Transport_fp_calculator:
    #Method that realices the calculus of the vehicule emissions
    def calculate_transport_emission(self, distance, consumed_fuel, old_emission_factor, cylinders_emission_factor,  fuel_emission_factor):            
        try:
            if consumed_fuel == 0:
                return jsonify({"error": "Consumed fuel cannot be zero"}), 400
            
            distance = float(distance)
            consumed_fuel = float(consumed_fuel)
            
            fuel_performance = round(distance / consumed_fuel, 2)
            
            fuel_consume = 1 / fuel_performance        
            
            transport_emission = distance * fuel_consume * fuel_emission_factor * (1 + cylinders_emission_factor + old_emission_factor)
            
            final_transport_emission = round(transport_emission, 2)
            
            return final_transport_emission
        except ValueError:
            return jsonify({"error": "Distance and consumed fuel must be numbers"}), 400


'''
def get_factors():
    pass
'''