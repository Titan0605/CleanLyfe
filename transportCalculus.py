#Method that realices the calculus of the vehicule emissions
def transportEmission(distance, consumed_fuel,old_emission_factor, cylinders_emission_factor,  fuel_emission_factor):            
    fuel_performance = round(distance / consumed_fuel, 2)
    
    fuel_consume = 1/ fuel_performance        
    
    final_transport_emission = distance * fuel_consume * fuel_emission_factor * (1 + cylinders_emission_factor + old_emission_factor)
    
    return final_transport_emission, fuel_performance        
