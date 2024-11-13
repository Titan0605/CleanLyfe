#Method that realices the calculus of the vehicule emissions
def vehicleEmission(distance, fuel, fuel_emission_factor, cylinders_emission_factor, old_emission_factor):            
    fuel_performance = distance / fuel
    
    fuel_consume = 1/ fuel_performance        
    
    final_transport_emission = distance * fuel_consume * fuel_emission_factor * (1 + cylinders_emission_factor + old_emission_factor)
    
    return final_transport_emission, fuel_performance        
  