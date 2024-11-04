#CacaCuloPedoPis
def vehicleEmission(distance, fuel, fuel_type, cylinders, old):
    #VARIABLES
    fuel_emission_factor = 0.0
    cylinder_adjustment = 0.0
    old_adjustment = 0
    #Kilómetros que el vehículo recorre por cada litro de combustible
    efficient = distance / fuel
    
    fuel_consume = 1/ efficient
    
    #
    match fuel_type:
        case 'gasoline':
            fuel_emission_factor = 2.31
            print(fuel_emission_factor)
        case 'diesel':
            fuel_emission_factor = 2.68
            print(fuel_emission_factor)
        case 'nature_gas':
            fuel_emission_factor = 2.79
            print(fuel_emission_factor)
        case 'electrical':
            fuel_emission_factor = 0.465
            print(fuel_emission_factor)
    
    #Creo que seria mejor cambiar a por un ifelse
    match cylinders:
        case cylinders if cylinders < 4:
            cylinder_adjustment = -0.05
            print(cylinder_adjustment)
        case 4:
            cylinder_adjustment = 0
            print(cylinder_adjustment)
        case 6:
            cylinder_adjustment = 0.10
            print(cylinder_adjustment)
        case _:
            cylinder_adjustment = 0
            print(cylinder_adjustment)
    
    match old:
        case old if (2024 - old )> 10:
            old_adjustment = 0.10
            print(old_adjustment)
        case old if (2024 - old) > 5 and (2024 - old) < 10:
            old_adjustment = 0.05
            print(old_adjustment)
        case old if (2024 - old) < 5:
            old_adjustment = 0
            print(old_adjustment)
        case _:
            old_adjustment = 0
            print(old_adjustment) 
    
    final_emission = distance * fuel_consume * fuel_emission_factor * (1 + cylinder_adjustment + old_adjustment)
    print(final_emission)    
    
    
print("alvrrrr")
vehicleEmission(200, 20, 'gasoline', 6, 2012)