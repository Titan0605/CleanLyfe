from flask import jsonify
from enum import Enum

class FuelAdjustment(Enum):
    GAS = ('Gas',  2.31)
    DIESEL = ('Diesel',  2.68)
    GNV = ('GNV',  2.79)
    ELECTRIC = ('Electric',  0.465)
    
    def __init__(self, id: str, carbon_emission: float) -> None:
        self.id: str = id
        self.carbon_emission: float = carbon_emission
    
class CylinderAdjustment(Enum):
    ECONOMIC = -0.05
    NORMAL = 0.0
    POWERFUL = 0.10
    
class YearAdjustment(Enum):
    NEW = 0.0
    USED = 0.05
    OLD = 0.10
    

class TransportCalculator:
    #Method that realices the calculus of the vehicule emissions
    def calculate_transport_footprint(self, distance: int, consumed_fuel: int, car_year: int, car_cylinders: int,  fuel_used: str):            
        try:
            if car_year is None and car_cylinders is None and fuel_used is None:
                return ({"error": "Missing parameters"})
            
            if distance > 0 and consumed_fuel == 0:
                return ({"error": "Consumed fuel cannot be zero when there is distance."})
            elif distance == 0 and consumed_fuel == 0:
                return 0
            try:
                fuel_adjustment = next(member.carbon_emission for member in FuelAdjustment if member.id == fuel_used)
            except StopIteration:
                return ({"error": f"Invalid product type. Must be one of: {[adjustment.id for adjustment in FuelAdjustment]}"})
            
            match car_year:
                case _ if car_year <= 5:
                    year_adjustment = YearAdjustment.NEW.value
                case _ if car_year <= 10:
                    year_adjustment = YearAdjustment.USED.value
                case _:
                    year_adjustment = YearAdjustment.OLD.value
                    
            match car_cylinders:
                case _ if car_cylinders < 4:
                    cylinder_adjustment = CylinderAdjustment.ECONOMIC.value
                case _ if car_cylinders == 4:
                    cylinder_adjustment = CylinderAdjustment.NORMAL.value
                case _ if car_cylinders >= 6:
                    cylinder_adjustment = CylinderAdjustment.POWERFUL.value
            
            fuel_performance = round(distance / consumed_fuel, 2)
            
            fuel_consume = 1 / fuel_performance     
            
            transport_emission = distance * fuel_consume * fuel_adjustment * (1 + cylinder_adjustment + year_adjustment)
            
            final_transport_emission = round(transport_emission, 2)
            
            transport_calculus = {
                "fuelUsed": fuel_used,
                "cylinderRating": car_cylinders,
                "vehicleYear": car_year,
                "timeUsedHours": "It needs to be added",
                "consumedFuel": consumed_fuel,
                "distanceTraveled": distance,
                "fuelPerfomance": fuel_performance,
                "totalEmission": final_transport_emission
            }
            
            return transport_calculus
        except ValueError:
            return {"error": "Something went wrong, try again later."}