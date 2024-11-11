#Method that realices the calculus of the vehicule emissions
def vehicleEmission(distance, fuel, fuel_emission_factor, cylinder_adjustment, old_adjustment):            
    fuel_performance = distance / fuel
    
    fuel_consume = 1/ fuel_performance
    
    final_transport_emission = distance * fuel_consume * fuel_emission_factor * (1 + cylinder_adjustment + old_adjustment)
    print(final_transport_emission)            